import json
import re

def multiply_query(llm_instance, query, n):
    prompt = f"""
        Você é um assistente especializado em gerar perguntas relacionadas a um determinado tema.
        Dada uma pergunta do usuário, gere exatamente {n} perguntas relevantes e relacionadas ao mesmo tema.
        Mantenha o foco no mesmo contexto, explorando ângulos diferentes.
        Retorne sem preâmbulos, títulos ou qualquer outro texto adicional.
        Retorne apenas um json com a lista de perguntas geradas no seguinte formato:
        
        ```json
            "perguntas": ["pergunta 1", "pergunta 2", "...", "pergunta n"]
        ```

        PERGUNTA:
        {query}
    """
    
    result = llm_instance.invoke(prompt)

    result = result[7:-4].strip()

    
    if result:
        try:
            data = json.loads(result)
            perguntas = data.get("perguntas", [])
        except json.JSONDecodeError:
            print("Erro ao decodificar JSON")
            perguntas = []
    else:
        print("JSON não encontrado na resposta")
        perguntas = []
    
    return [query] + perguntas
