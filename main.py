from fastapi import FastAPI
from pydantic import BaseModel
from config import Config
from llm.dspy_llm import DSPyLLM
from patterns.DSP import DSP
from patterns.RAGFusion import RAGFusion
from patterns.self_rag.SelfRAG import SelfRAG
from retriever.retriever import Retriever
from retriever.dspy_retriever import DSPyRetriever
from retriever.reranker import Reranker
from llm.llm import LLM
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

@app.post("/rag-fusion")
async def chat(request: ChatRequest):
    answer = RAGFusion().call(
        query=request.query,
        model=model,
        retriever_class=retriever_class,
        retriever=retriever,
        reranker_class=reranker_class,
        reranker=reranker,
        llm=llm_class
    )
    
    return answer

@app.post("/dsp")
async def chat(request: ChatRequest):
    answer = DSP().call(
        query=request.query,
        dspy=dspy,
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
