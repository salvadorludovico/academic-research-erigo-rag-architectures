from langchain_core.messages import HumanMessage, SystemMessage
from config import Config

def expand_query_by_multiple_query_method(llm, query, n):
    system_message = """
        Você é um assistente especializado em gerar perguntas relacionadas a um determinado tema.
        Dado uma pergunta, sua tarefa é gerar outras {n} perguntas relevantes e relacionadas.
        Mantenha o foco no mesmo contexto e gere variações que possam explorar ângulos diferentes do mesmo tema.
        Se a pergunta não fizer sentido ou for muito específica, mantenha a coerência ao gerar variações.
        Retorne apenas as queries separadas por quebra de linha
    """

    prompt = f"""
        Dada a pergunta abaixo, gere {n} perguntas diferentes, mas relacionadas ao mesmo contexto:

        PERGUNTA:
        {query}
    """

    messages = [
        SystemMessage(content=system_message),
        HumanMessage(content=prompt),
    ]

    prompt = f"""
        Você é um assistente especializado em gerar perguntas relacionadas a um determinado tema.
        Dado uma pergunta, sua tarefa é gerar outras {n} perguntas relevantes e relacionadas.
        Mantenha o foco no mesmo contexto e gere variações que possam explorar ângulos diferentes do mesmo tema.
        Se a pergunta não fizer sentido ou for muito específica, mantenha a coerência ao gerar variações.
        
        Retorne apenas as queries separadas por quebra de linha. Não adicione preâmbulos ou explicações.	

        Dada a pergunta abaixo, gere {n} perguntas diferentes, mas relacionadas ao mesmo contexto:

        PERGUNTA:
        {query}
    """


    # result = llm.llm_generate_batch(model_name=Config().OPENAI_LLM_MODEL, messages=messages)
    result = llm.llm_generate_batch(model_name=Config().GEMINI_MODEL, prompt=prompt)

    # generated_queries = result[0].content.strip().split("\n")
    generated_queries = result.strip().split("\n")
    
    return [query] + generated_queries