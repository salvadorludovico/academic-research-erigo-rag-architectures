from utils.check_sim_nao import check_sim_nao

def is_document_relevant(llm_instance, query, document):
    prompt = f"""Você é um avaliador analisando a relevância de um documento recuperado para uma pergunta do usuário.
      Não precisa ser um teste rigoroso. O objetivo é filtrar recuperações errôneas.
      Se o documento contiver palavra(s)-chave ou um significado semântico relacionado à pergunta do usuário, classifique-o como relevante.
      Responda apenas com "sim" ou "não" para indicar se o documento é relevante para a pergunta, sem nenhum outro comentário ou explicação.

      Documento recuperado:

      {document}

      Pergunta do usuário: {query}
    """
    
    result = llm_instance.invoke(prompt)
    result = check_sim_nao(result)
    
    return result