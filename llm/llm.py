from langchain_google_vertexai import VertexAI

class LLM:
    def llm_instance(self, model_name):
        llm = VertexAI(model_name=model_name, project="energygpt-421317", temperature=0.5)
        return llm

    def llm_generate_stream(self,model_name,prompt):
     
        instance_llm = self.llm_instance(model_name)
        for chunk in instance_llm.stream(prompt):
            yield chunk

    def llm_generate(self,model_name,prompt):
        instance_llm = self.llm_instance(model_name)
        return instance_llm.invoke(prompt)