import os
import concurrent.futures
from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents import AgentType
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from query_validator import QueryValidator,is_complex_sentence
from config import GROQ_API_KEY,LANGCHAIN_API_KEY

os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = "true"

def init_database(user: str, password: str, host: str, port: str, database: str, db_type: str = "postgresql"):
    try:
        db_type = db_type.lower()

        if db_type == "postgresql":
            db_uri = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        elif db_type == "mysql":
            db_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        elif db_type == "sqlite":
            db_uri = f"sqlite:///{database}"
        elif db_type == "oracle":
            db_uri = f"oracle+cx_oracle://{user}:{password}@{host}:{port}/{database}"
        elif db_type == "mssql":
            db_uri = f"mssql+pyodbc://{user}:{password}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
        elif db_type == "postgresql_psycopg2":
            db_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

        db = SQLDatabase.from_uri(db_uri, sample_rows_in_table_info=3)
        return db

    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def get_table_info(db):
    result = db.table_info
    return result



def generate_response_with_agent(user_query: str, db: SQLDatabase, chat_history: list):
    print("Enter inside the Agent-based SQL chain")
    agent_executor = create_sql_agent(
        llm=ChatGroq(
            api_key=GROQ_API_KEY,
            model_name="llama3-70b-8192",
            temperature=0
        ),
        db=db,
        agent_type="openai-tools",
        verbose=False,
        stream_runnable=False,
        handle_parsing_errors=True
    )
    response = agent_executor.invoke(user_query)
    return response['output']

def get_sql_chain(db):
    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's PostgreSQL database.
    Based on the table schema below, write a SQL query that would answer the user's question. Take the conversation history into account.

    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}

    Write only the SQL query and nothing else. Do not wrap the SQL query in any other text, not even backticks.

    For example:
    Question: which 3 artists have the most tracks?
    SQL Query: SELECT ArtistId, COUNT(*) as track_count FROM Track GROUP BY ArtistId ORDER BY track_count DESC LIMIT 3;
    Question: Name 10 artists
    SQL Query: SELECT Name FROM Artist LIMIT 10;

    Your turn:

    Question: {question}
    SQL Query:
    """

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name="llama3-70b-8192",
        temperature=0
    )

    def get_schema(_):
        return get_table_info(db)

    return (
        RunnablePassthrough.assign(schema=get_schema)
        | prompt
        | llm
        | StrOutputParser()
    )

def generate_response_with_chain(user_query: str, db, chat_history: list):
    sql_chain = get_sql_chain(db)

    template = """
    You are a data analyst at a company. You are interacting with a user who is asking you questions about the company's database.
    Based on the table schema below, question, sql query, and sql response, write a natural language response.
    <SCHEMA>{schema}</SCHEMA>

    Conversation History: {chat_history}
    SQL Query: <SQL>{query}</SQL>
    User question: {question}
    SQL Response: {response}"""

    prompt = ChatPromptTemplate.from_template(template)

    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name="llama3-8b-8192",
        temperature=0
    )

    def run_sql_query(query):
      results = db.run(query)
      if not results  or results == "" :
        return "No results found."
      return results

    chain = (
        RunnablePassthrough.assign(query=sql_chain).assign(
            schema=lambda _: get_table_info(db),
            response=lambda vars: run_sql_query(vars["query"]),
        )
        | prompt
        | llm
        | StrOutputParser()
    )
    print("Enter inside the Normal SQL chain")
    return chain.invoke({
        "question": user_query,
        "chat_history": chat_history,
    })
    
    
# Function to execute response generation functions with a Time Limit
def generate_response_with_timeout(func, user_query, db, chat_history, timeout=120):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(func, user_query, db, chat_history)
        try:
            return future.result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            return None
        except Exception as e:
            print(f"Error occurred in generate_response_with_timeout: {e}")
            return None

def get_response(user_query: str, db, chat_history: list):
    validator = QueryValidator()
    
    # Validate the query
    validation_message = validator.validate_query(user_query)
    if validation_message != "Query is valid.":
        return validation_message

    # Check if the sentence is complex
    is_complex = is_complex_sentence(user_query)

    # Choose the initial function based on complexity
    initial_func = generate_response_with_agent if is_complex else generate_response_with_chain
    fallback_func = generate_response_with_chain if initial_func == generate_response_with_agent else generate_response_with_agent

    # Attempt to get response from the initial function
    response = generate_response_with_timeout(initial_func, user_query, db, chat_history)
    if response is not None:
        return response

    # If the initial function times out, try the fallback function
    response = generate_response_with_timeout(fallback_func, user_query, db, chat_history)
    if response is not None:
        return response

    return "Please rewrite the query with more proper clarity"
