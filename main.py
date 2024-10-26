from fastapi import FastAPI
from pydantic import BaseModel
from config import Config
from patterns.RAGFusion import RAGFusion
from retriever.retriever import Retriever
from retriever.reranker import Reranker
from llm.llm import LLM

app = FastAPI()

retriever_class = Retriever()
reranker_class = Reranker()
llm_class = LLM()

vectorstore = retriever_class.vectorstore_instance()
retriever = retriever_class.retriever_instance(vectorstore)
reranker = reranker_class.reranker_instance()
model = Config().GEMINI_MODEL



class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
