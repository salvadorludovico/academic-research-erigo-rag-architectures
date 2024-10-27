from prompt.prompt import prompt_generator

class NaiveRAG:
  def call(self, query, retriever_class, retriever, llm_instance):

    print("----------EXECUTING NaiveRAG----------")
    print("--->RETRIEVING DOCUMENTS")
    retrieved_documents = retriever_class.retrieve(retriever, query)
    print(f"{len(retrieved_documents)}" + " retrieved documents")

    print("--->GENERATING ANSWER")
    prompt = prompt_generator().get_generation_prompt(query=query, context=retrieved_documents)
    answer = llm_instance.invoke(prompt)
    
    response = {
      "query": query,
      "answer": answer,
      "context": retrieved_documents,
    }

    print (answer)
    return response