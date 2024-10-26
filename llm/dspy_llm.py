import os
import dspy
import google.generativeai as genai
from config import Config

class DSPyLLM(dspy.LM):
  def __init__(self, model, api_key=None, endpoint=None, **kwargs):
    config = Config()
    SERVICE_ACCOUNT_PATH = config.SERVICE_ACCOUNT_PATH

    if SERVICE_ACCOUNT_PATH:
      os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SERVICE_ACCOUNT_PATH
    else:
      return "SERVICE_ACCOUNT_PATH not found"
    
    genai.configure()

    self.endpoint = endpoint
    self.history = []

    super().__init__(model, **kwargs)
    self.model = genai.GenerativeModel(model)

  def __call__(self, prompt=None, messages=None, **kwargs):
      prompt = '\n\n'.join([x['content'] for x in messages] + ['BEGIN RESPONSE:'])

      completions = self.model.generate_content(prompt)
      self.history.append({"prompt": prompt, "completions": completions})

      return [completions.candidates[0].content.parts[0].text]

  def inspect_history(self):
      for interaction in self.history:
          print(f"Prompt: {interaction['prompt']} -> Completions: {interaction['completions']}")

lm = DSPyLLM("gemini-pro", temperature=0.5)
dspy.configure(lm=lm)

qa = dspy.ChainOfThought("question->answer")
qa(question="What is the capital of France?")