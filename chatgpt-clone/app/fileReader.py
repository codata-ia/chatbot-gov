import os
import datetime

numeroConversas = len(os.listdir("conversation"))
nome_arquivo = "arquivo_conversa_" + datetime.date.today().strftime("%Y-%m-%d") + "-" + str(numeroConversas)
caminho_arquivo = os.path.join("conversation", nome_arquivo)

def saveConversation(user_message, chatbot_message):
    with open(caminho_arquivo, 'a', encoding='utf-8') as file:
        file.write(f"usuario: \"{user_message}\"\n")
        file.write(f"chatbot: \"{chatbot_message.replace('\n', ' ')}\"\n")
    return

def getSystemMessage():
    with open('processData/servicosGerais.txt', 'r', encoding='utf-8') as file:
        document_content = file.read()
        system_message = {"role": "system", "content": f"Contexto: {document_content}"}
    return system_message

def getCssStyle():
    with open("app/style/styles.css", "r") as file:
        css_string = file.read()
    return css_string