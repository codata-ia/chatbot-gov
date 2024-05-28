import os
import datetime


def getSystemMessage():
    with open('processData/servicosGerais.txt', 'r', encoding='utf-8') as file:
        document_content = file.read()
        system_message = {"role": "system", "content": f"Contexto: {document_content}"}
    return system_message