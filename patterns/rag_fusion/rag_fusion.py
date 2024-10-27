from query_manipulator.multiply_query import multiply_query
from prompt.prompt import prompt_generator
from config import Config

class RAGFusion:
  def call(self, query, model, retriever_class, retriever, reranker_class, reranker, llm_instance):
    config = Config()

    print("----------EXECUTING RAGFusion----------")
    print("--->EXPANDING QUERIES")
    query_expansions = multiply_query(llm_instance, query, config.QUERY_EXPANSION_NUMBER)
    
    for q in query_expansions:
      print("-> " + q)

    print("--->RETRIEVING DOCUMENTS IN PARALLEL")
    retrieved_documents = retriever_class.retrieve_in_parallel(retriever, query_expansions)
    print(f"{len(retrieved_documents)}" + " retrieved documents")

    print("--->RERANKING DOCUMENTS")
    reranked_documents = reranker_class.rerank_documents(reranker, retrieved_documents, query)
    
    print("--->GENERATING ANSWER")
    prompt = prompt_generator().get_generation_prompt(query=query, context=reranked_documents)
    answer = llm_instance.invoke(prompt)

    response = {
      "query": query,
      "answer": answer,
      "context": reranked_documents,
    }

    print (answer)
    return response