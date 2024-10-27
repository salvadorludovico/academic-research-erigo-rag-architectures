def multiply_query(llm_instance, query, n):
    prompt = f"""
        Você é um assistente especializado em gerar perguntas relacionadas a um determinado tema.
        Dada uma pergunta, gere exatamente {n} perguntas relevantes e relacionadas ao mesmo tema.
        Mantenha o foco no mesmo contexto, explorando ângulos diferentes.
        Retorne estritamente cada pergunta em uma nova linha, sem numeração, sem símbolos, sem preâmbulos, títulos ou qualquer outro texto adicional. 

        PERGUNTA:
        {query}
    """

    
    result = llm_instance.invoke(prompt)

    generated_queries = result.strip().split("\n")
    
    return [query] + generated_queries