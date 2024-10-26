from langchain_chroma import Chroma
from langchain_google_vertexai import VertexAIEmbeddings
import os, concurrent.futures
from config import Config

class Retriever:
  def __init__(self):
    self.config = Config()

  def vectorstore_instance(self):
    persist_directory = f"./data/chroma/{self.config.CASE}"

    embedding_function = VertexAIEmbeddings(model_name=self.config.RETRIEVER_VERTEX_MODEL)

    if os.path.exists(persist_directory) and os.listdir(persist_directory):
      vectorstore = Chroma(
        collection_name=self.config.CASE,
        persist_directory=persist_directory,
        embedding_function=embedding_function
      )
    else:
      print("VectorStore não encontrado.")
      raise FileNotFoundError("VectorStore não encontrado.")
    
    return vectorstore
  
  def retriever_instance(self, vectorstore):    
    retriever = vectorstore.as_retriever(
      search_type = self.config.RETRIEVER_SEARCH_TYPE,
      search_kwargs = {"k": self.config.RETRIEVER_TOP_K}
    )
    
    return retriever
    
  def retrieve(self, retriever, query):
    documents = retriever.invoke(query)

    return documents
  
  def retrieve_in_parallel(self, retriever, queries):
    retrieved_documents = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(self.retrieve, retriever, query) for query in queries]

        for future in concurrent.futures.as_completed(futures):
            retrieved_documents.extend(future.result())

    return retrieved_documents