# BackendAPI para a CODATA

Essa é uma API backend desenvolvida utilizando o Flask framework. 
Esse projeto consiste em uma aplicação backend para tratar dos modelos
descritos pela pela empresa CODATA.

## Pré-requisitos 
- Git
- Vscode
- Python
- Pip
- Flask

## Instalação(Windows)

Passos para instalar o projeto localmente. Isso pode incluir a clonagem do repositório, a instalação de dependências e outras configurações de banco de dados necessárias.

1º Clonar o projeto

2º Usar o comando abaixo para instalar os pacotes e dependências.
```
pip install -r requirements.txt
```

## Como usar

A rota abaixo é consumida no front-end para receber uma requisição POST com um campo de mensgem para o chatbot responder

```
{
    "message": "Mensagem para o chatbot"
}
```

```
http://localhost:5000/predict
```