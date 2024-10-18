from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from config import Config

class Reranker:
  def __init__(self):
    self.config = Config()

  def reranker_instance(self):
    model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")

    reranker = CrossEncoderReranker(
        model=model,
        top_n=self.config.RETRIEVER_RERANKING_TOP_N
    )

    return reranker

  def rerank_documents(self, reranker, documents, query):
    reranked_documents = reranker.compress_documents(documents, query)

    return reranked_documents