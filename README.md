Antes de executar o programa, criar um arquivo chamado constants.py para usar a API KEY e também dados sobre o banco de dados
db_driver = "psycopg" - Driver para fazer a conexão com o postgre
db_host = "localhost"
db_port = "5432" - Porta utilizada pelo postgre criada na configuração do banco de dados
db_name =  - Nome do banco de dados onde vão ser armazenadas as tabelas
db_user =  - Nome do usuário para fazer a conexão
db_password = - Senha para fazer a conexão

Executar o arquivo database_connection depois de fazer essas configurações para criar os embeddings com os servicos disponíveis na pasta data

Agora é só executar o arquivo app.py para poder fazer um prompt e obter a resposta