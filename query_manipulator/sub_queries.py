def generate_sub_queries(llm_instance, query, n):
    prompt = f"""
        Você é um assistente útil que gera consultas de pesquisa com base em uma única pergunta de entrada.

        Realize a decomposição da consulta. Dada uma pergunta do usuário, divida-a em subperguntas distintas que precisam ser respondidas para responder à pergunta original.

        Se houver acrônimos ou palavras com as quais você não está familiarizado, não tente reformulá-los.

        Pergunta: {query}
    """

    
    result = llm_instance.invoke(prompt)

    generated_queries = result.strip().split("\n")
    
    return [query] + generated_queries