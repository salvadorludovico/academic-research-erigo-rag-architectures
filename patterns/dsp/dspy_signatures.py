import dspy
# Signature
# - Componente que define o objetivo da tarefa que a LLM deve resolver
# - Fornece também algumas descrições dos dados de entrada e saída (Input/Output Fields)
# - Acredito que podemos adicionar outros inputs além dos padrões (context, question)

class GenerateAnswer(dspy.Signature):
    """Responda as perguntas com respostas detalhadas baseadas no contexto."""

    context = dspy.InputField(desc="deve conter fatos relevantes")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="responda de forma detalhada e pode permitir textos longos")