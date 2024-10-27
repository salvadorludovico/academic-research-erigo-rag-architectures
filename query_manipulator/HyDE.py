def generate_hyde(llm_instance, query):
    prompt = f"""
        Você é especialista do Tribunal de Contas do Estado de Goiás (TCEGO) responsável por escrever documentos que contenham informações a repeito do topico {query}.
        Sua resposta deve ser abrangente e incluir todos os pontos-chave que estariam presentes no principal resultado de busca.

        Retorne apenas o texto do documento.
    """
    
    result = llm_instance.invoke(prompt)

    return result