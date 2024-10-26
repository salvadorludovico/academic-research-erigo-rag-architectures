def grade_answer(llm_instance, query, generation):
    prompt = f"""Você é um avaliador que verifica se uma resposta aborda ou resolve uma pergunta.
      Responda apenas com uma palavra: 'sim' se a resposta atende plenamente à pergunta ou 'não' se não atende. Não forneça explicações adicionais.

      Pergunta do usuário: {query}

      Geração do LLM: {generation}
    """
    
    result = llm_instance.invoke(prompt)
    
    return result