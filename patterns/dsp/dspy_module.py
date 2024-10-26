import dspy
from patterns.dsp.dspy_signatures import GenerateAnswer

# Module
# - É responsável pela definição das camadas/passos, ou melhor, da PIPELINE
class Predict(dspy.Module):
    def __init__(self, num_passages=3):
        super().__init__()

        self.retrieve = dspy.Retrieve(k=num_passages)
        self.generate_answer = dspy.ChainOfThought(GenerateAnswer)

    async def forward(self, question, context):
        # context = await self.retrieve(question).passages
        prediction = await self.generate_answer(context=context,question=question)
        return dspy.Prediction(context=context,answer=prediction.answer)