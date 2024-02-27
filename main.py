from openai import OpenAI
import gradio as gr
from dotenv import load_dotenv
import os
import utils.convert_json as cj
import json

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(os.path.join(os.getcwd(), 'config', '.env'))

# Agora você pode acessar sua chave da OpenAI como uma variável de ambiente
openai_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key= openai_key)

context = json.loads(cj.ler_texto_de_arquivo("process_data/processoRenovacaoCNH.json"))
    
def user(user_message, history):
    return "", history + [[user_message, None]]
    
def predict(history):
    history_openai_format = []
    history_openai_format.append(context)
    for human, assistant in history:
        history_openai_format.append({"role": "user", "content": human })
        if(assistant != None):
            history_openai_format.append({"role": "assistant", "content":assistant})
    #history_openai_format.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model='gpt-3.5-turbo-1106',
        messages= history_openai_format,
        temperature = 0.7,
        stream=True
    )

    history[-1][1] = ""
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            history[-1][1] = history[-1][1] + chunk.choices[0].delta.content
            yield history
            
def upload_file(files, history):
        file_paths = [file.name for file in files]        
        return history + [[file_paths, None]]
    
theme= gr.themes.Soft(primary_hue="sky",
                        secondary_hue="neutral",
                        neutral_hue="cyan",
                    ).set(
                        background_fill_primary='#3a89c9',
                        background_fill_primary_dark='#0f2f4e'
                    )

with gr.Blocks(theme= theme, css="front/gradio.css") as demo:
    gr.Image(value = "https://detran.pb.gov.br/imagens/imagens-detran/detran-pb.png/@@images/ccf2a27c-e576-48a9-8f58-e9ec637035b7.png",width="300px",label=None, show_download_button= False, show_label=False,elem_classes="logo")
    with gr.Column(variant="compact"):
        chatbot = gr.Chatbot(label="Chat")
        with gr.Row(variant="compact"):
            with gr.Column(scale=15):
                msg = gr.Textbox(placeholder="Digite aqui sua duvida", autofocus= True, show_label=False, min_width=500)
            with gr.Column(min_width=5, elem_classes= "buttons"):
                submit = gr.Button("➥",elem_classes="button")
                
                upload_button = gr.UploadButton("📁", file_types=["image", "video"], file_count="multiple",elem_classes="button", visible= False)
                
            def clean_textbox():
                return ""
            
            gr.on(
                triggers=[msg.submit, submit.click],
                fn=user,
                inputs=[msg, chatbot],
                outputs=[msg, chatbot],
            ).then(predict,[chatbot], [chatbot])            
            
            upload_button.upload(upload_file, [upload_button, chatbot] , [chatbot]
            ).then(predict,[chatbot], [chatbot])
            

demo.launch(share = False, debug=True)

#3a89c9
#0f2f4e