from fastapi import FastAPI
from pydantic import BaseModel
from config import Config

from llm.llm import LLM
from llm.dspy_llm import DSPyLLM

from retriever.retriever import Retriever
from retriever.reranker import Reranker
from retriever.dspy_retriever import DSPyRetriever

from patterns.naive_rag.naive_rag import NaiveRAG
from patterns.naive_hyde_rag.naive_hyde_rag import NaiveHyDERAG
from patterns.crag_hyde.crag_hyde import CRAGHyDE
from patterns.rag_fusion.rag_fusion import RAGFusion
from patterns.self_rag.self_rag import SelfRAG
from patterns.dsp.dsp import DSP

import dspy

app = FastAPI()

# RAGFusion
retriever_class = Retriever()
reranker_class = Reranker()
llm_class = LLM()
llm_instance = llm_class.llm_instance(Config().GEMINI_MODEL)

vectorstore = retriever_class.vectorstore_instance()
retriever = retriever_class.retriever_instance(vectorstore)
reranker = reranker_class.reranker_instance()
model = Config().GEMINI_MODEL

# Dspy
dspy_llm = DSPyLLM(model)
dspy_retriever = DSPyRetriever()
dspy.configure(lm=dspy_llm, rm=dspy_retriever)

class ChatRequest(BaseModel):
    query: str

@app.post("/naive-rag")
async def chat(request: ChatRequest):
    answer = NaiveRAG().call(
        query=request.query,
        retriever_class=retriever_class,
        retriever=retriever,
        llm_instance=llm_instance
    )

    return answer

@app.post("/naive-hyde-rag")
async def chat(request: ChatRequest):
    answer = NaiveHyDERAG().call(
        query=request.query,
        retriever_class=retriever_class,
        retriever=retriever,
        llm_instance=llm_instance
    )

    return answer

@app.post("/crag-hyde")
async def chat(request: ChatRequest):
    answer = CRAGHyDE().call(
        query=request.query,
        retriever_class=retriever_class,
        retriever=retriever,
        llm_instance=llm_instance
    )

    return answer


@app.post("/rag-fusion")
async def chat(request: ChatRequest):
    answer = RAGFusion().call(
        query=request.query,
        model=model,
        retriever_class=retriever_class,
        retriever=retriever,
        reranker_class=reranker_class,
        reranker=reranker,
        llm_instance=llm_instance
    )
    
    return answer

@app.post("/self-rag")
async def chat(request: ChatRequest):
    answer = SelfRAG().call(
        query=request.query,
        retriever_class=retriever_class,
        retriever=retriever,
        llm_instance=llm_instance
    )

    return answer

@app.post("/dsp")
async def chat(request: ChatRequest):
    answer = DSP().call(
        query=request.query,
        dspy=dspy,
        retriever=retriever
    )
    
    return answer

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
