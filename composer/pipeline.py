from langchain_core.messages import HumanMessage, SystemMessage
from input_manager.query_expander import expand_query_by_multiple_query_method

class AdvancedRAG:
  def call(self, query, model, retriever_class, retriever, reranker_class, reranker, llm):

    query_expansions = expand_query_by_multiple_query_method(llm, query, 3)
    print("QUERY EXPANSIONS")
    print(query_expansions)
    print("QUERY EXPANSIONS")
    retrieved_documents = retriever_class.retrieve_in_parallel(retriever, query_expansions)
    print("RETRIEVED DOCUMENTS")
    print("RETRIEVED DOCUMENTS")
    print("RETRIEVED DOCUMENTS")
    reranked_documents = reranker_class.rerank_documents(reranker, retrieved_documents, query)
    print("RERANKED DOCUMENTS")
    print("RERANKED DOCUMENTS")
    print("RERANKED DOCUMENTS")
      
    system_message= """
      Seu nome é Iago e você é um assistente muito útil para tarefas de pergunta e resposta e tem acesso à uma base de legislações do Tribunal de Contas do Estado de Goiás (TCE GO).
      Você é muito cordial e utiliza-se de expressões elegantes para dar as respostas.

      Se você não sabe a resposta, basta dizer que não sabe. Use o máximo de detalhamento que a pergunta exija.
    """

    human_message = f"""
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

    
    result = llm.llm_generate_batch(model, messages)

    print("RESULT")

    response = {
      "query": query,
      "context": reranked_documents,
      "answer": result[0].content
    }

    print(response)

    return response