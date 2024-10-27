from patterns.self_rag.is_document_relevant import is_document_relevant
from prompt.prompt import prompt_generator
from query_manipulator.HyDE import generate_hyde

class CRAGHyDE:
  def call(self, query, retriever_class, retriever, llm_instance):

    print("----------EXECUTING CRAG HyDE----------")
    print("--->RETRIEVING DOCUMENTS")
    retrieved_documents = retriever_class.retrieve(retriever, query)
    print(f"{len(retrieved_documents)}" + " retrieved documents")

    print("--->GRADING DOCUMENTS")
    relevant_docs = [];
    for index, doc in enumerate(retrieved_documents):
      is_relevant = is_document_relevant(llm_instance, query, doc)
      print(f"-> DOC {index + 1} RELEVANT: {is_relevant}")
      if is_relevant:
        relevant_docs.append(doc)
    
    if not relevant_docs:
      print("--->REPLACE QUERY WITH HyDE (HYPOTHETHICAL DOCUMENT EMBEDDINGS)")
      HyDE = generate_hyde(llm_instance, query)
      print(f"-> HyDE: {HyDE}")
      relevant_docs = retriever_class.retrieve(retriever, HyDE)

    print("--->GENERATING ANSWER w/ relevant docs")
    prompt = prompt_generator().get_generation_prompt(query=query, context=relevant_docs)
    answer = llm_instance.invoke(prompt)
    
    response = {
      "query": query,
      "answer": answer,
      "context": relevant_docs,
    }

    print (answer)
    return response