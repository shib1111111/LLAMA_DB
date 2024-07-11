from langchain_groq import ChatGroq
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from config import GROQ_API_KEY,NVIDIA_API_KEY


groq_llama3_8b = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name="llama3-8b-8192",
        temperature=0
    )

groq_llama3_70b = ChatGroq(
        api_key=GROQ_API_KEY,
        model_name="llama3-70b-8192",
        temperature=0
    )

nvidia_llama3_70b = ChatNVIDIA(
    model="meta/llama2-70b",
    nvidia_api_key = NVIDIA_API_KEY
    )