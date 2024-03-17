import gradio as gr

logo = "https://detran.pb.gov.br/imagens/imagens-detran/detran-pb.png/@@images/ccf2a27c-e576-48a9-8f58-e9ec637035b7.png"
#3a89c9 azul claro
#0f2f4e azul escuro
#D2D7D3 cinza 
#EBF20F amarelo 
theme = gr.themes.Soft(
    primary_hue="sky",
    neutral_hue="cyan",
).set(
    body_background_fill_dark='#0f2f4e',
    border_color_primary_dark='#EBF20F'
)

title = "DetranBot"