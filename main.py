from fastapi import FastAPI
from pydantic import BaseModel
from config import Config
from composer.RAGFusion import RAGFusion
from retriever.retriever import Retriever
from retriever.reranker import Reranker
# from llm.llm import LLM
from llm.llm import LLMGoogleVertexAI

app = FastAPI()

retriever_class = Retriever()
reranker_class = Reranker()
# llm_class = LLM()
llm_class = LLMGoogleVertexAI()

vectorstore = retriever_class.vectorstore_instance()
retriever = retriever_class.retriever_instance(vectorstore)
reranker = reranker_class.reranker_instance()
# import GEMINI_MODEL from config
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
