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

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY

system_message = {"role": "system", "content": "You are an agent of Detran of Paraiba\nYour taks is to always answer like a typical assistant to help people with doubts on some services in Detran\nAlways be kind and try to do your best to answer\n\nYour name is Detrinho, and you have a passion to help people.\nYour principal activity is Renovação de CNH."}

css = ".wrapper {background: url('file=chatgpt-clone/images/detranBackgroudWhite.jpg'); background-size: cover; background-position: center}"

translatorEnToPt = Translator(provider='libre', from_lang='en', to_lang='pt')

translatorPtToEn = Translator(provider='libre', from_lang='pt', to_lang='en')

with gr.Blocks(css=css) as demo:
    loader = TextLoader('chatgpt-clone/processData/cnhRenovationProcess.txt', encoding="utf8")
    loader.load()
    index = VectorstoreIndexCreator().from_loaders([loader])

    chatbot = gr.Chatbot(label="Chatbot do Detran-PB")
    msg = gr.Textbox(label="Caixa de texto", placeholder="Digite a sua dúvida")
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

demo.launch(allowed_paths=list("chatgpt-clone/images/detranBackgroudWhite.jpg"))