from langchain_openai import ChatOpenAI
from langchain_google_vertexai import VertexAI
from config import Config

class LLM:
    def llm_instance(self, model_name):
        llm = ChatOpenAI(model=model_name, api_key=Config().OPEN_AI_API_KEY)
        return llm

    def llm_generate_stream(self, model_name, messages):
        chat = self.llm_instance(model_name)

        for chunk in chat.stream(messages):
            yield chunk.content

    def llm_generate_batch(self, model_name, messages):
        chat = self.llm_instance(model_name)

        return chat.batch([messages])

class LLMGoogleVertexAI:
    def llm_instance(self, model_name): # gemini-pro
        llm = VertexAI(model_name=model_name, project="energygpt-421317")
        return llm

    def llm_generate_stream(self,model_name,prompt):
     
        instance_llm = self.llm_instance(model_name)
        for chunk in instance_llm.stream(prompt):
            yield chunk

    def llm_generate_batch(self,model_name,prompt):
        instance_llm = self.llm_instance(model_name)
        return instance_llm.invoke(prompt)