from dotenv import load_dotenv
import os
from google.auth import load_credentials_from_file

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
  os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# GOOGLE_APPLICATION_CREDENTIALS
SERVICE_ACCOUNT_PATH = os.getenv("SERVICE_ACCOUNT_PATH")
if SERVICE_ACCOUNT_PATH:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_PATH

class Config:
    OPENAI_LLM_MODEL = os.getenv("OPENAI_LLM_MODEL")
    OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL")
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP"))
    PROJECT_PATH = os.getenv("PROJECT_PATH")
    DOCUMENTS_SOURCE = os.getenv("DOCUMENTS_SOURCE")
    
    RETRIEVER_EMBEDDING_MODEL = os.getenv("RETRIEVER_EMBEDDING_MODEL")
    RETRIEVER_SEARCH_TYPE = os.getenv("RETRIEVER_SEARCH_TYPE")
    RETRIEVER_TOP_K = int(os.getenv("RETRIEVER_TOP_K"))
    RETRIEVER_RERANKING_TOP_N = int(os.getenv("RETRIEVER_RERANKING_TOP_N"))
    RETRIEVER_VERTEX_MODEL = os.getenv("RETRIEVER_VERTEX_MODEL")

    QUERY_EXPANSION_NUMBER = int(os.getenv("QUERY_EXPANSION_NUMBER"))
    SERVICE_ACCOUNT_PATH = os.getenv("SERVICE_ACCOUNT_PATH")
    GOOGLE_CREDENTIALS = load_credentials_from_file(SERVICE_ACCOUNT_PATH)
    VERTEX_API_KEY = os.getenv("VERTEX_API_KEY")
    
    
    CASE = os.getenv("CASE")
