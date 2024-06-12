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
- PostgreSQL

## Instalação(Windows)

Passos para instalar o projeto localmente. Isso pode incluir a clonagem do repositório, a instalação de dependências e outras configurações de banco de dados necessárias.

1º Clonar o projeto

2º Usar o comando abaixo para instalar os pacotes e dependências.
```
pip install -r requirements.txt
```

## Como usar

Antes de executar o programa, criar um arquivo chamado constants.py para usar a API KEY e também dados sobre o banco de dados
- db_driver = "psycopg" - Driver para fazer a conexão com o postgre
- db_host = "localhost"
- db_port = "5432" - Porta utilizada pelo postgre criada na configuração do banco de dados
- db_name =  "Nome do banco de dados onde vão ser armazenadas as tabelas"
- db_user = "Nome do usuário para fazer a conexão"
- db_password = "Senha para fazer a conexão"

Executar o arquivo database_connection depois de fazer essas configurações para criar os embeddings com os servicos disponíveis na pasta que contém os arquivos txt

```
python database_connection.py
```

Executar app.py para inicializar a API

```
python app.py
```

A rota abaixo é consumida no front-end para receber uma requisição POST com um campo de mensgem para o chatbot responder

```
{
    "message": "Mensagem para o chatbot"
}
```

```
http://localhost:5000/predict
```


