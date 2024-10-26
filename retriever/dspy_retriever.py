import chromadb
from langchain_google_vertexai import VertexAIEmbeddings
import os
from dspy.retrieve.chromadb_rm import ChromadbRM
import chromadb.utils.embedding_functions as embedding_functions
from config import Config

class DSPyRetriever:
  def __init__(self):
    self.config = Config()
    self.persist_directory = f"./data/chroma/{self.config.CASE}"

  def vectorstore_instance(self):
    if os.path.exists(self.persist_directory) and os.listdir(self.persist_directory):
      persisted_chroma_client = chromadb.PersistentClient(path=self.persist_directory)
      vectorstore = persisted_chroma_client.get_or_create_collection(name="legis")
    else:
      print("VectorStore não encontrado.")
      raise FileNotFoundError("VectorStore não encontrado.")
    
    return vectorstore
  
  def retriever_instance(self):
    # embedding_function = VertexAIEmbeddings(model_name=self.config.RETRIEVER_VERTEX_MODEL)
    embedding_function  = embedding_functions.GoogleGenerativeAiEmbeddingFunction(model_name=self.config.RETRIEVER_VERTEX_MODEL, credentials=self.config.GOOGLE_CREDENTIALS)

    retriever = ChromadbRM(
      'legis',
      self.persist_directory,
      embedding_function = embedding_function,
      k = self.config.RETRIEVER_TOP_K
    )
    
    return retriever
    
  def retrieve(self, retriever, query):
    documents = retriever(query)

    return documents