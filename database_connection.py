from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_postgres.vectorstores import PGVector
from dotenv import load_dotenv

import os
import constants
load_dotenv()

DATA_PATH = "detran_updated_services"
# os.environ["OPENAI_API_KEY"] = constants.OPENAI_API_KEY

os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

def main():
    generate_data_store()

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_db(chunks)

def load_documents():

    #Ser trocado pela API depois 
    loader = DirectoryLoader(DATA_PATH, glob="*.txt")
    documents = loader.load()
    return documents

def split_text(documents):
    #Divisão do texto em chunks para transformá-los em vetores, o tamanho do chunk foi calculado usando uma aproximação do tamanho dos serviços
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500, 
        chunk_overlap=300,
    )
    texts = text_splitter.split_documents(documents=documents)
    return texts

def save_to_db(chunks):

    #Criação do modelo de embeddings usando langchain
    embeddings = get_embeddings()

    #Conexão com o Banco de Dados
    COLLECTION_NAME = get_collection_name()

    #Cria a string de conexão com o banco de dados
    CONNECTION_STRING = get_connection_string()

    #Faz a conexão com o banco de dados
    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=COLLECTION_NAME,
        connection=CONNECTION_STRING,
        use_jsonb=True,
        pre_delete_collection=True,
    )
    
    #Adiciona os documentos no baco de dados
    vectorstore.add_documents(documents=chunks)

def get_similarity_results(query):
    vectorstore = PGVector(
        embeddings = get_embeddings(),
        collection_name = get_collection_name(),
        connection = get_connection_string(),
        use_jsonb = True,
    )
    return vectorstore.similarity_search(query, k = 3)

def get_embeddings():
    return OpenAIEmbeddings(model="text-embedding-3-small")

def get_collection_name():
    return "Servicos_Gerais"

def get_connection_string():
    CONNECTION_STRING = PGVector.connection_string_from_db_params(
        driver = os.getenv("db_driver"), 
        host = os.getenv("db_host"), 
        port = os.getenv("db_port"), 
        database = os.getenv("db_name"), 
        user = os.getenv("db_user"), 
        password= os.getenv("db_password")
    )
    return CONNECTION_STRING

if __name__ == "__main__":
    main()