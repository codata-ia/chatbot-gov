from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

import os
import constants
from database_connection import get_similarity_results


os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY

DATA_PATH = "data"

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

def main():
    #Texto para usar no GPT
    query_text = input("Digite a sua dúvida para o chatbot: ")
    results = get_similarity_results(query_text)

    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0.1)
    response_text = model.predict(prompt)
    print(response_text)

if __name__ == "__main__":
    main()