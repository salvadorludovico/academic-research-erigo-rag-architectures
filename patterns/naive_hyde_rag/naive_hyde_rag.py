from query_manipulator.HyDE import generate_hyde
from prompt.prompt import prompt_generator

class NaiveHyDERAG:
  def call(self, query, retriever_class, retriever, llm_instance):

    print("----------EXECUTING NaiveRAG with HyDE----------")
    print("--->GENERATE HyDE (HYPOTHETHICAL DOCUMENT EMBEDDINGS)")

    HyDE = generate_hyde(llm_instance, query)

    # Here we have two options: only HyDE or HyDE + query 

    print("--->RETRIEVING DOCUMENTS")
    retrieved_documents = retriever_class.retrieve(retriever, HyDE)
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