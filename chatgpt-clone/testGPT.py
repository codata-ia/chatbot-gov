from openai import OpenAI
import os
import constants

os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY

client = OpenAI()

def testConversation(tema, json, fluxoInteracao):
    reponse = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "Vai ser fornecido para você um tema, um json e um fluxo de interação quero que você elabore duas notas de 0 a 1, uma calculando quantos '%' o chatbot no fluxo de interação está falando sobre o tema informado e se as respostas do chatbot no fluxo de interação corresponde as etapas descritas no json, eu quero que você me informe somente as notas, exemplo, nota tema: e nota resposta: "},
            {"role": "user", "content": f"Tema: {tema}, json: {json} e fluxo de interação: {fluxoInteracao}, elabore para mim uma nota para cada correspondência"}
        ]
    )

    return reponse.choices[0].message.content


jsonTest = {
  "setor": "detran",
  "area": "habilitação",
  "serviço": "renovar a carteira",
  "etapas": {
    "1": "Preencher formulário de solicitação",
    "2": "Agendar exame médico",
    "3": "Realizar exame psicotécnico",
    "4": "Efetuar pagamento da taxa de renovação",
    "5": "Retirar nova carteira de habilitação"
  },
  "fonte": "https://endereçopublico.com/lasdjfalsdf"
}

for nome_arquivo in os.listdir("conversation"):
    nota1= testConversation("Renovação CNH", jsonTest, "conversation/" + nome_arquivo)
    print(nota1)