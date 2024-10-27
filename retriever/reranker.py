from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from transformers import AutoConfig, AutoModel
from FlagEmbedding import FlagReranker
from config import Config

class Reranker:
  def __init__(self):
    self.config = Config()

  def reranker_instance(self):
    model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-base")
    # model = HuggingFaceCrossEncoder(model_name="bge-reranker-v2-m3")
    # model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-minicpm-layerwise", trust_remote_code=True)
    # config = AutoConfig.from_pretrained("BAAI/bge-reranker-v2-minicpm-layerwise", trust_remote_code=True)
    # model = HuggingFaceCrossEncoder(config=config)

    reranker = CrossEncoderReranker(
        model=model,
        top_n=self.config.RETRIEVER_RERANKING_TOP_N
    )

    return reranker

  def rerank_documents(self, reranker, documents, query):
    reranked_documents = reranker.compress_documents(documents, query)

    return reranked_documents
  
  def reranker_instance_flag(self):
    reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)

    return reranker
  
  def rerank_documents_flag(self, reranker, documents, query):
    top_n = self.config.RETRIEVER_RERANKING_TOP_N

    docs = [str(doc.page_content) for doc in documents]
    
    doc_pairs = [[query, doc] for doc in docs]
    
    documents_score = reranker.compute_score(doc_pairs)

    scored_documents = list(zip(docs, documents_score))

    top_documents = sorted(scored_documents, key=lambda x: x[1], reverse=True)[:top_n]

    return [doc for doc, score in top_documents]