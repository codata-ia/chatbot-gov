import gradio as gr
import openai
import time
import os

from langchain_community.document_loaders import TextLoader
from langchain_community.chat_models import ChatOpenAI
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain_community.vectorstores import Chroma

from translate import Translator

import constants

import datetime

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY

system_message = {"role": "system", "content": "You are an agent of Detran of Paraiba\nYour task is to always answer like a typical assistant to help people with doubts on some services in Detran\nAlways be kind and try to do your best to answer\n\nYour name is Detrinho, and you have a passion to help people.\n"}

"""
theme = gr.themes.Soft(
        primary_hue="sky",
        secondary_hue="neutral",
        neutral_hue="cyan",
        ).set(
            background_fill_primary='#3a89c9',
            background_fill_primary_dark='#0f2f4e'
)
"""

css = """
    .gradio-container-4-16-0 {background-color: white;}
    .wrapper.svelte-nab2ao {background-color: white;
    border: solid 8px;
    border-color: darkgrey;
    }
    label.svelte-1b6s6s{background-color: #ff4949;
    border-radius: 5px;
    position: static;
    margin-top: 5px;
    margin-left: 5px;
    color: white;
    border-color: #ff4949;
    }
    .scroll-hide svelte-1f354aw{background-color: white;}
    .user.svelte-1lcyrx4.svelte-1lcyrx4.svelte-1lcyrx4{background-color: #07542b;}
    .bot.svelte-1lcyrx4.svelte-1lcyrx4.svelte-1lcyrx4{background-color: #2484c6;}
    .block.svelte-90oupt{background-color: darkgrey;}
    textarea.svelte-1f354aw.svelte-1f354aw{background-color: white;
    color:black;
    }
    .pending.svelte-1gpwetz{
    background-color: darkgrey;
    }
    span.svelte-1gfkn6j:not(.has-info) {
    margin-bottom: var(--spacing-lg);
    color: white;
    }
    *{border: none;}
    .divisoria-colorida-governo {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
    height: 14px;
    position: relative;
    width: 100%;
    }
"""

with gr.Blocks(css=css) as demo:
    
    #Salvar conversa em arquivo de texto
    numeroConversas = len(os.listdir("conversation"))

    nome_arquivo = "arquivo_conversa_" + datetime.date.today().strftime("%Y-%m-%d") + "-" + str(numeroConversas)

    caminho_arquivo = os.path.join("conversation", nome_arquivo)

    title = gr.HTML("<div class='divisoria-colorida-governo'><div class='cor-1' style='background-color: #ffeb36;'></div><div class='cor-2' style='background-color: #f72930;'></div><div class='cor-3' style='background-color: #399fe8;'></div><div class='cor-4' style='background-color: #00dc58;'></div><div class='cor-5' style='background-color: #0f0a0a;'></div></div><div style='text-align: center; background-color: white;'><img src='https://paraiba.pb.gov.br/imagens/imagens-site/marca-stp/Govpb.png/@@images/abaa40cc-5d26-41fc-bc49-1e4679d05a79.png' style='display: block; margin: auto;  width: 300px;'></div>")
    
    loader = TextLoader('processData/servicosGerais.txt', encoding="utf8")
    loader.load()
    index = VectorstoreIndexCreator().from_loaders([loader])

    chatbot = gr.Chatbot(label="Chatbot")
    msg = gr.Textbox(label="Caixa de texto", placeholder="Digite a sua dúvida", )
    clear = gr.Button("Reiniciar conversa")

    state = gr.State([])

    def user(user_message, history):
        return "", history + [[user_message, None]]

    def bot(history, messages_history):
        user_message = history[-1][0]
        bot_message, messages_history = ask_gpt(user_message, messages_history)
        #messages_history += [{"role": "assistant", "content": bot_message}]
        history[-1][1] = bot_message
        time.sleep(1)
        return history, messages_history

    def ask_gpt(message, messages_history):
        #messages_history += [{"role": "user", "content": message}]
        """
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=messages_history,
            top_p=1
        )
        """
        #Carrega o langchain e aplica o modelo para responder de acordo com 
        """ SE FOR USADO O MODELO COM CHATOPENAI, ELE MUDA MUITO DE CONTEXTO, APLICAS APLICANDO O LLM ELE SE DETEM AO BÁSICO, 
        QUE É O QUE ESTÁ ESCRITO NO TXT, ELE POR EXEMPLO DIZ QUE A PESSOA DEVE CONSULTAR O SITE DO DETRAN, PARA MAIS INFORMAÇÕES INVÉS DE SÓ RESPONDER

        chain = ConversationalRetrievalChain.from_llm(llm=ChatOpenAI(model="gpt-3.5-turbo-1106"), 
        retriever = index.vectorstore.as_retriever(search_kwargs={"k":1}),
        )
        response = chain({"question": message, "chat_history": messages_history})
        messages_history.append((message, response['answer']))
        return response['answer'], messages_history
        """

        messages_history.append((message, index.query(message)))
        with open(caminho_arquivo, 'a', encoding='utf-8') as f:
            f.write(f"usuario: \"{message}\"\n")
            f.write(f"chatbot: \"{index.query(message).replace('\n', ' ')}\"\n")
        return index.query(message), messages_history 
        #return response.choices[0].message.content, messages_history

    def init_history(messages_history):
        messages_history = []
        messages_history.append((system_message,None))
        return messages_history

    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, [chatbot, state], [chatbot, state]
    )

    clear.click(lambda: None, None, chatbot, queue=False).success(init_history, [state], [state])

demo.launch()