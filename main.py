from openai import OpenAI
import gradio as gr
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(os.path.join(os.getcwd(), 'config', '.env'))

# Agora você pode acessar sua chave da OpenAI como uma variável de ambiente
openai_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key= openai_key)

def predict(message, history, temperature=0.7):
    history_openai_format = []
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        history_openai_format.append({"role": "assistant", "content":assistant})
    history_openai_format.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages= history_openai_format,
        temperature = temperature,
        stream=True
    )


    partial_message = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            partial_message = partial_message + chunk.choices[0].delta.content
            yield partial_message

chat = gr.ChatInterface(predict).queue()
chat.launch(share = True, debug=True)