def rewrite_query(llm_instance, query):
    prompt = f"""Você é um reformulador de perguntas que converte uma pergunta de entrada em uma versão melhorada, otimizada para recuperação em um vetor. 
      Analise a pergunta de entrada e infera a intenção ou significado semântico subjacente. Retorne apenas a pergunta aprimorada, sem explicações adicionais.

      Pergunta inicial: {query}

      Pergunta aprimorada:
    """

    result = llm_instance.invoke(prompt)
    
    return result