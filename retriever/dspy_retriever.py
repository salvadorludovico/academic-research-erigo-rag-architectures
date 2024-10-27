import chromadb
from langchain_google_vertexai import VertexAIEmbeddings
import os
from dspy.retrieve.chromadb_rm import ChromadbRM
from langchain_chroma import Chroma
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
    embedding_function = VertexAIEmbeddings(model_name=self.config.RETRIEVER_VERTEX_MODEL)
    # embedding_function  = embedding_functions.GoogleVertexEmbeddingFunction(model_name=f"models/{self.config.RETRIEVER_VERTEX_MODEL}", api_key=self.config.VERTEX_API_KEY)
    # embedding_function  = embedding_functions.GoogleVertexEmbeddingFunction(api_key=self.config.VERTEX_API_KEY)
    # embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction(api_key=self.config.VERTEX_API_KEY)

    def get_embeddings(docs_array):
      embedding_function = VertexAIEmbeddings(model_name=self.config.RETRIEVER_VERTEX_MODEL)
      return embedding_function.embed_documents(docs_array)

    retriever = ChromadbRM(
      'legis',
      self.persist_directory,
      embedding_function = get_embeddings,
      k = self.config.RETRIEVER_TOP_K
    )
    
    return retriever
    
  def retrieve(self, retriever, query):
    documents = retriever(query)

    return documents