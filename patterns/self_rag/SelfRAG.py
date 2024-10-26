from patterns.self_rag.document_grader import grade_document
from patterns.self_rag.answer_grader import grade_answer
from patterns.self_rag.hallucinations_grader import grade_hallucinations
from patterns.self_rag.query_rewriter import rewrite_query

from prompt.prompt import prompt_generator
from config import Config

class SelfRAG:
  def call(self, query, retriever_class, retriever, llm_instance):
    config = Config()

    print("----------EXECUTING SelfRAG----------")
    print("--->RETRIEVING DOCUMENTS")
    retrieved_documents = retriever_class.retrieve(retriever, query)
    print(f"{len(retrieved_documents)}" + " retrieved documents")

    print("--->GRADING DOCUMENTS")
    relevant_docs = [];
    for index, doc in enumerate(retrieved_documents):
      grade = grade_document(llm_instance, query, doc)
      print(f"-> DOC {index + 1} GRADE: {grade}")
      if grade == "sim":
        relevant_docs.append(doc)
    
    if not relevant_docs:
      print("--->REWRITING QUERY")
      new_query = rewrite_query(llm_instance, query)
      print(f"-> Rewritten query: {new_query}")
      query = new_query
      relevant_docs = retriever_class.retrieve(retriever, new_query)

    print("--->GENERATING ANSWER w/ relevant docs")
    prompt = prompt_generator().get_generation_prompt(query=query, context=relevant_docs)
    answer = llm_instance.invoke(prompt)

    print("--->CHECKING FOR HALLUCINATIONS")
    hallucination_check = grade_hallucinations(llm_instance, relevant_docs, answer)
    if hallucination_check == "não":
      print("-> Answer contains hallucinations. Regenerating...")
      answer = prompt_generator(llm_instance, query, relevant_docs)

    print("--->VERIFYING ANSWER")
    answer_relevance = grade_answer(llm_instance, query, answer)
    if answer_relevance == "não":
      print("Answer does not fully address the question. Regenerating...")
      answer = prompt_generator(llm_instance, query, relevant_docs)
    
    response = {
      "query": query,
      "answer": answer,
      "context": relevant_docs,
    }

    print (answer)
    return response