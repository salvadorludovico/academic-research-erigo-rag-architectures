from langchain_core.messages import HumanMessage, SystemMessage
from input_manager.query_expander import expand_query_by_multiple_query_method

class RAGFusion:
  def call(self, query, model, retriever_class, retriever, reranker_class, reranker, llm):

    case = "Tribunal de Contas do Estado de Goiás (TCE GO)"

    print("----------EXECUTING RAGFusion----------")
    print("--->EXPANDING QUERIES")
    query_expansions = expand_query_by_multiple_query_method(llm, query, 3)
    
    for q in query_expansions:
      print("- " + q)

    print("--->RETRIEVING DOCUMENTS IN PARALLEL")
    retrieved_documents = retriever_class.retrieve_in_parallel(retriever, query_expansions)
    print(f"{len(retrieved_documents)}" + " retrieved documents")

    print("--->RERANKING DOCUMENTS")
    reranked_documents = reranker_class.rerank_documents(reranker, retrieved_documents, query)
    

    print("--->GENERATING ANSWER")
    system_message= """
      Você é um assistente muito útil para tarefas de pergunta e resposta e tem acesso à uma base de legislações do Tribunal de Contas do Estado de Goiás (TCE GO).

      Se você não sabe a resposta, basta dizer que não sabe. Use o máximo de detalhamento que a pergunta exija.
    """

    human_message = f"""
      Com base no contexto recuperado, responda à pergunta de forma amigável e completa.

      PERGUNTA:
      {query}

      CONTEXTO:
      {reranked_documents}
    """

    prompt = f"""
      Você é um assistente muito útil para tarefas de pergunta e resposta e tem acesso à uma base de legislações do Tribunal de Contas do Estado de Goiás (TCE GO).

      Se você não sabe a resposta, basta dizer que não sabe. Use o máximo de detalhamento que a pergunta exija.

      Com base no contexto recuperado, responda à pergunta de forma amigável e completa.

      PERGUNTA:
      {query}

      CONTEXTO:
      {reranked_documents}
    """

    messages = [
      SystemMessage(content=system_message),
      HumanMessage(content=human_message),
    ]

    
    # result = llm.llm_generate_batch(model, messages)
    result = llm.llm_generate_batch(model, prompt)

    print("RESULT")

    response = {
      "query": query,
      "context": reranked_documents,
      "answer": result
    }

    print(response)

    return response