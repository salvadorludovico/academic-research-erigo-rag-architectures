from patterns.self_rag.is_document_relevant import is_document_relevant
from patterns.self_rag.answer_checker import does_answer_fit_query
from patterns.self_rag.hallucination_checker import is_answer_fundamented
from patterns.self_rag.query_rewriter import rewrite_query
from prompt.prompt import prompt_generator

class SelfRAG:
  def call(self, query, retriever_class, retriever, llm_instance):
    original_query = query

    print("----------EXECUTING SelfRAG----------")
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
      print("--->REWRITING QUERY")
      new_query = rewrite_query(llm_instance, query)
      print(f"-> Rewritten query: {new_query}")
      query = new_query 
      relevant_docs = retriever_class.retrieve(retriever, query)

    print("--->GENERATING ANSWER w/ relevant docs")
    prompt = prompt_generator().get_generation_prompt(query=query, context=relevant_docs)
    answer = llm_instance.invoke(prompt)

    print("--->CHECKING FOR HALLUCINATIONS")
    is_fundamented = is_answer_fundamented(llm_instance, relevant_docs, answer)
    if is_fundamented == False:
      print("-> Answer contains hallucinations. Regenerating...")
      prompt = prompt_generator().get_generation_prompt(query=query, context=relevant_docs)
      answer = llm_instance.invoke(prompt)

    print("--->VERIFYING ANSWER")
    does_answer_fit = does_answer_fit_query(llm_instance, query, answer)
    if does_answer_fit == False:
      print("Answer does not fully address the question. Regenerating...")
      prompt = prompt_generator().get_generation_prompt(query=query, context=relevant_docs)
      answer = llm_instance.invoke(prompt)
    
    response = {
      "query": original_query,
      "answer": answer,
      "context": relevant_docs,
    }

    print (answer)
    return response