from config import Config

def expand_query_by_multiple_query_method(llm, query, n):
    prompt = f"""
        Você é um assistente especializado em gerar perguntas relacionadas a um determinado tema.
        Dada uma pergunta, gere exatamente {n} perguntas relevantes e relacionadas ao mesmo tema.
        Mantenha o foco no mesmo contexto, explorando ângulos diferentes.
        Retorne apenas as perguntas, cada uma em uma linha, sem preâmbulos, numeração, símbolos, explicações ou qualquer outro texto adicional.

        PERGUNTA:
        {query}
    """
    
    result = llm.llm_generate(model_name=Config().GEMINI_MODEL, prompt=prompt)

    generated_queries = result.strip().split("\n")
    
    return [query] + generated_queries