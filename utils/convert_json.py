import json

def ler_texto_de_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        return arquivo.read()

def converter_para_json(texto):
    texto_com_quebra_de_linha = texto.replace('\n',';')
    return {"role": "system", "content": texto_com_quebra_de_linha}

def salvar_json(json_data, nome_arquivo_saida):
    with open(nome_arquivo_saida, 'w', encoding='utf-8') as arquivo_saida:
        json.dump(json_data, arquivo_saida, ensure_ascii=False, indent=4)

def main():
    nome_arquivo_entrada = 'process_data/processoRenovacaoCNH.txt'  # Coloque o nome do seu arquivo de entrada aqui
    nome_arquivo_saida = 'process_data/processoRenovacaoCNH.json'  # Nome do arquivo de saída JSON

    texto = ler_texto_de_arquivo(nome_arquivo_entrada)
    json_data = converter_para_json(texto)
    salvar_json(json_data, nome_arquivo_saida)
    print("Texto convertido para JSON e salvo em", nome_arquivo_saida)

if __name__ == "__main__":
    main()
