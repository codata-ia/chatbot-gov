import time
import gradio as gr

def chat_response(message, history):    
    response = "Voce digitou: "
    if not message:
        response = ""
        message = "Não vai digitar nada?"     
    sleeptime = 0.5/len(message)
    for i in range(len(message)):
        time.sleep(sleeptime)
        yield response + message[: i+1]
    
    
gr.ChatInterface(chat_response).launch()