import constants
import os
import json
from langchain.prompts import ChatPromptTemplate
from openai import OpenAI
from database_connection import get_similarity_results

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

# os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY

PROMPT_TEMPLATE = """
Responda a questão baseando-se somente no contexto a seguir:
Você é um chatbot do Governo da Paraiba e deve seguir as seguintes diretrizes:
- Tente soar o mais natural possível, quando for responder alguma dúvida ou qualquer tipo de texto e sempre em português brasileiro
- Você deve seguir o contexto a seguir e estritamente ele, não cabe a você responder qualquer outro tipo de pergunta que não seja desse contexto
- Quando responder uma dúvida ou pergunta sobre algum serviço cite de qual setor ele é, se é detran por exemplo, e de qual área é, se é habilitação ou veiculo, a área e o serviço estão especificados no contexto abaixo
- Sempre citar as etapas numericamente em ordem conforme são apresentadas ao usuário

{context}

---

Answer the question based on the above context: {question}
"""

client = OpenAI()

model = "gpt-3.5-turbo-0125"

def processMessage(user_message, messages_history):
    results = get_similarity_results(user_message)

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=user_message)
    
    messages_history += [{"role": "user", "content": prompt}]

    chatbot_response = getBotResponse(messages_history)
    
    messages_history += [{"role": "assistant", "content": chatbot_response}]
    
    return chatbot_response, messages_history

def getBotResponse(messages_history):
    response = client.chat.completions.create(
        model = model,
        messages = messages_history,
        temperature = 0.1
    )
    return response.choices[0].message.content
