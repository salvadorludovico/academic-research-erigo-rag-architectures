from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import os, concurrent.futures
from config import Config

class Retriever:
  def __init__(self):
    self.config = Config()
  def vectorstore_instance(self):
    persist_directory = "./data/chroma"

    embedding = OpenAIEmbeddings(
      model=self.config.RETRIEVER_EMBEDDING_MODEL,
      api_key=self.config.OPEN_AI_API_KEY
    )

    if os.path.exists(persist_directory) and os.listdir(persist_directory):
      vectorstore = Chroma(
        collection_name="legis",
        persist_directory=persist_directory,
        embedding_function=embedding
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