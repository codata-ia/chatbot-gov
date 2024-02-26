import gradio as gr
import random
import time   

def respond(message, chat_history):
    bot_message = random.choice(["How are you?", "I love you", "I'm very hungry"])
    chat_history.append((message, bot_message))
    time.sleep(2)
    return chat_history

def upload_file(files, chat_history):
    file_paths = [file.name for file in files]
    return respond(file_paths, chat_history)
css="""
.buttons{
    width: 35px;
}
.button {
    height: 35px;    
}
.textbox{
    height: 85px;
}
 """
with gr.Blocks(theme= gr.themes.Soft(
                            primary_hue="sky",
                            secondary_hue="neutral",
                            neutral_hue="cyan",
                        ).set(
                            background_fill_primary='#3a89c9',
                            background_fill_primary_dark='#0f2f4e'
                        ),css=css) as demo:
    gr.Image(value = "https://detran.pb.gov.br/imagens/imagens-detran/detran-pb.png/@@images/ccf2a27c-e576-48a9-8f58-e9ec637035b7.png",width="300px",label=None, show_download_button= False, show_label=False,elem_classes="logo")
    with gr.Column(variant="compact"):
        chatbot = gr.Chatbot(label="Chat")
        with gr.Row(variant="compact"):
            with gr.Column(scale=15):
                msg = gr.Textbox(placeholder="Digite aqui", autofocus= True, show_label=False, min_width=500,elem_classes="textbox",lines=2)
            with gr.Column(elem_classes="buttons", min_width=25):
                submit = gr.Button("➥",elem_classes="button")
                
                upload_button = gr.UploadButton("📁", file_types=["image", "video"], file_count="multiple",elem_classes="button")
                
            def clean_textbox():
                return ""
            
            gr.on(
                triggers=[msg.submit, submit.click],
                fn=respond,
                inputs=[msg, chatbot],
                outputs=[chatbot],
            ).then(clean_textbox, outputs=[msg])
            
            upload_button.upload(upload_file, [upload_button, chatbot] , [chatbot]) 
            

demo.launch()