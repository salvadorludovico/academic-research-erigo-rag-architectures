from utils.check_sim_nao import check_sim_nao

def is_answer_fundamented(llm_instance, documents, generation):
    prompt = f"""Você é um avaliador analisando se a geração de um LLM é fundamentada em / apoiada por um conjunto de fatos recuperados.
      Dê uma pontuação binária 'sim' ou 'não'. 'Sim' significa que a resposta está fundamentada / apoiada pelo conjunto de fatos.

      Responda apenas com "sim" ou "não" sem qualquer comentário adicional.

      Conjunto de fatos:

      {documents}

      Geração do LLM: {generation}
    """
    
    result = llm_instance.invoke(prompt)
    result = check_sim_nao(result)
    
    return result