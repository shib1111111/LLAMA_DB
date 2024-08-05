import streamlit as st
import requests


# Backend server URL
#SERVER_URL = "https://10.184.61.103:8443"
#SERVER_URL = "https://llama-db.onrender.com"
SERVER_URL = "https://absms.cdacchn.in:8443"


# SSL CERTIFICATE
CERTIFICATE_PATH = 'cert.pem'

class AIMessage:
    def __init__(self, content):
        self.content = content
    def to_dict(self):
        return {"type": "AIMessage", "content": self.content}

class HumanMessage:
    def __init__(self, content):
        self.content = content
    def to_dict(self):
        return {"type": "HumanMessage", "content": self.content}

def initialize_session_state():
    if "access_token" not in st.session_state:
        st.session_state.access_token = None
    if "page" not in st.session_state:
        st.session_state.page = "authentication"
    if "api_key" not in st.session_state:
        st.session_state.api_key = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content="Hello! I'm a SQL assistant. Ask me anything about your database."),
        ]

def login(username, password):
    response = requests.post(f"{SERVER_URL}/login", data={"username": username, "password": password}, verify=False)
    if response.status_code == 200:
        st.session_state.access_token = response.json()["access_token"]
        st.success("Login successful!")
        st.session_state.page = "main"
        st.rerun()
    else:
        st.error("Login failed. Please check your credentials.")

def signup(username, password):
    response = requests.post(f"{SERVER_URL}/signup", json={"username": username, "password": password},verify=False)
    if response.status_code == 200:
        st.session_state.access_token = response.json()["access_token"]
        st.success("Signup successful!")
        st.session_state.page = "main"
        st.rerun()
    else:
        st.error("Signup failed. User may already exist.")

def generate_api_key():
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.post(f"{SERVER_URL}/api_key", headers=headers,verify=False)
    if response.status_code == 200:
        st.success(f"Generated API key: {response.json()['api_key']}")
    else:
        st.error("Failed to generate API key.")

def list_api_keys():
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.get(f"{SERVER_URL}/api_keys", headers=headers, verify=False)
    if response.status_code == 200:
        api_keys = response.json().get("api_keys", [])
        if not api_keys:
            st.info("No API keys found.")
            return
        st.success("Your API keys:")
        for api_key in api_keys:
            st.write(api_key)
    else:
        st.error("Failed to fetch API keys.")


def connect_to_db(host, port, user, password, database):
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    try:
        response = requests.post(f"{SERVER_URL}/connect", json={
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database
        }, headers=headers, verify=False)

        if response.status_code == 200:
            st.session_state.db_connected = True
            st.sidebar.success("Connected to database!")
        else:
            st.session_state.db_connected = False
            st.sidebar.error(response.json().get("detail", "Connection failed"))
    except Exception as e:
        st.session_state.db_connected = False
        st.sidebar.error(str(e))

def query_db(query):
    try:
        headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
        serialized_history = [msg.to_dict() for msg in st.session_state.chat_history]
        payload = {
            "api_key": st.session_state.api_key,
            "query": query,
            "chat_history": serialized_history
        }
        response = requests.post(f"{SERVER_URL}/query", headers=headers, json=payload, verify=False)
        if response.status_code == 200:
            response_content = response.json()["response"]
            response_content =  response_content.split("Ahmedabad!", 1)[-1].strip()
            st.session_state.chat_history.append(HumanMessage(content=query))
            st.session_state.chat_history.append(AIMessage(content=response_content))
            st.markdown(response_content)
        else:
            st.error(f"Query failed:\n{response.json().get('detail', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

def authentication_page():
    st.subheader("User Authentication")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login"):
            login(username, password)
    with col2:
        if st.button("Signup"):
            signup(username, password)

def api_key_page():
    st.subheader("API Key")
    if st.button("Generate API Key"):
        generate_api_key()
    if st.button("Show API Keys"):
        list_api_keys()

def main_page():
    st.sidebar.subheader("Connect to the Database")

    host = st.sidebar.text_input("Host", value="10.184.43.111")
    port = st.sidebar.text_input("Port", value="5432")
    user = st.sidebar.text_input("User", value="postgres")
    password = st.sidebar.text_input("Password", type="password", value="postgres")
    #database = st.sidebar.text_input("Database", value="chatdb")
    db_names = [
        'postgres', 'star0224', 'examdb', 'icg2022offnov', 'icg2022sailnov', 
        'agnipath2023', 'navy_old', 'navy', 'afcat23feb', 'icgmar2023', 
        'icgmar2023_off', 'agnipathmay2023', 'navyjuly', 'afcataug2023', 
        'rhb1', 'agnipathoct2023', 'icg_today', 'rhb_today', 'agnipath_today', 
        'rhb_Nov22', 'agnipathOne', 'agnipathTwo', 'agnipathThree', 
        'agnipathFour', 'aiimsnov23', 'icgoffnov23', 'icmrnov23', 
        'icgsailnov23', 'dcmpr_hallticket_29_01_2024', 'dcmpr_hallticket_31_01_2024', 
        'afcat0224', 'icmr2024feb', 'nios2024feb', 'health_pic', 
        'exam_statistics', 'icgapr2024', 'icgapr2024sail', 'access_log_analysis', 
        'rp2406', 'dmpr2407', 'caqm2407', 'chatdb', 'dmprtest', 'nios2408', 'nios240805'
    ]
    
    database = st.sidebar.selectbox("Database", options=db_names)
    if st.sidebar.button("Connect"):
        connect_to_db(host, port, user, password, database)
    st.sidebar.subheader("Enter API Key")
    st.session_state.api_key = st.sidebar.text_input("API Key", value=st.session_state.api_key)
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
    user_query = st.chat_input("Type a message...")
    if user_query is not None and user_query.strip() != "":
        with st.chat_message("Human"):
            st.markdown(user_query)
        with st.chat_message("AI"):
            query_db(user_query)
            

def navbar():
    col1, col2, col3= st.columns(3)
    with col1:
        if st.button("Home"):
            st.session_state.page = "main"
            st.rerun()
    with col2:
        if st.button("API Key"):
            st.session_state.page = "api_key"
            st.rerun()
    with col3:
        if st.button("Logout"):
            st.session_state.access_token = None
            st.session_state.page = "authentication"
            st.rerun()


def main():
    st.set_page_config(page_title="Chat with SQL", layout="centered")
    st.markdown("<h1 style='text-align: center;'>Chat with SQL</h1>", unsafe_allow_html=True)
    initialize_session_state()
    if st.session_state.access_token:
        navbar()
        if st.session_state.page == "main":
            main_page()
        elif st.session_state.page == "api_key":
            api_key_page()
    else:
        authentication_page()

if __name__ == "__main__":
    main()
