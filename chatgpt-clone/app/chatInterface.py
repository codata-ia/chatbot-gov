import gradio as gr
import time

from aiProcessing import processMessage #importando a parte de processamento
from fileReader import getCssStyle, getSystemMessage


with gr.Blocks(css=getCssStyle()) as demo:
    
    def init_history(messages_history):
        messages_history = []
        messages_history += [getSystemMessage()]
        return messages_history

    def makeInterface():
        title = gr.HTML("<div class='divisoria-colorida-governo'><div class='cor-1' style='background-color: #ffeb36;'></div><div class='cor-2' style='background-color: #f72930;'></div><div class='cor-3' style='background-color: #399fe8;'></div><div class='cor-4' style='background-color: #00dc58;'></div><div class='cor-5' style='background-color: #0f0a0a;'></div></div><div style='text-align: center; background-color: white;'><img src='https://paraiba.pb.gov.br/imagens/imagens-site/marca-stp/Govpb.png/@@images/abaa40cc-5d26-41fc-bc49-1e4679d05a79.png' style='display: block; margin: auto;  width: 300px;'></div>")
        chatbot = gr.Chatbot(label="Chatbot")
        msg = gr.Textbox(label="Caixa de texto", placeholder="Digite a sua dúvida", )
        clear = gr.Button("Reiniciar conversa")
        return title, chatbot, msg, clear

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history, messages_history):
        user_message = history[-1][0]
        bot_message, messages_history = processMessage(user_message, messages_history) #No arquivo aiProcessing
        history[-1][1] = bot_message
        time.sleep(1)
        return history, messages_history

    state = gr.State([])
    state.value = init_history(state)

    title, chatbot, msg, clear = makeInterface()

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, [chatbot, state], [chatbot, state]
    )

    clear.click(lambda: None, None, chatbot, queue=False).success(init_history, [state], [state])