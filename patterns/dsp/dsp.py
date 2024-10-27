from config import Config
from patterns.dsp.dspy_module import Predict
from retriever.dspy_retriever import DSPyRetriever
import re

class DSP:
  def __init__(self):
    self.predict = Predict()
    self.config = Config()
    self.retriever = DSPyRetriever()

  def parse_response(self, response):
    context_match = re.search(r"Context:\s*(.*?)\n\n", response, re.DOTALL)
    query_match = re.search(r"Question:\s*(.*?)\n\n", response, re.DOTALL)
    answer_match = re.search(r"Answer:\s*(.*)", response, re.DOTALL)

    context = context_match.group(1).strip() if context_match else None
    query = query_match.group(1).strip() if query_match else None
    answer = answer_match.group(1).strip() if answer_match else None

    response = {
      "query": query,
      "answer": answer,
      "dspy_context": context,
    }

    return response
    
  def call(self, query, dspy, retriever):
    rm = self.retriever.retriever_instance()

    context = self.retriever.retrieve(rm, query)

    response = dspy.predict(query, context)

    parsed_response = self.parse_response(response.answer)
    
    response = {
      "query": query,
      "answer": parsed_response["answer"],
      "context": context,
      "dspy_context": parsed_response["dspy_context"],
    }

    print (response.answer)
    return response