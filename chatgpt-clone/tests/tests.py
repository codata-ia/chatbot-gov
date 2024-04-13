#Spacy
#Fuzz 
from thefuzz import fuzz

import spacy
import statistics
import os

nlp = spacy.load('pt_core_news_sm')

def testConversation(tema, json, fluxoInteracao):
    #Guardar variável com nota_tema e nota_resposta para fazer uma média e etc
    nota_tema = []
    nota_resposta = []
    with open(fluxoInteracao, 'r', encoding = 'utf-8') as arquivo:     #Ler Arquivo 
        mensagem_usuario = ""
        mensagem_chatbot = ""

        for linha in arquivo: #Tratar o arquivo
            linha = linha.strip()

            if(linha.startswith("usuario:")):
                mensagem_usuario = linha[len("usuario:") + 1:]
            
            elif(linha.startswith("chatbot:")):
                mensagem_chatbot = linha[len("chatbot:") + 1:]
            
            if mensagem_chatbot: #Fazer um loop que leia a cada duas interações 
                nota_tema.append(fuzz.token_set_ratio(mensagem_chatbot, tema) * 0.05) #Usar fuzz para calcular sobre o tema token_set_ratio
                
                nota_resposta_individual = []
                
                for procedimento in json["etapas"].items(): #Fazer um loop que passe por cada etapa de uma atividade
                    procedimento_nlp = nlp(procedimento[1])
                    mensagem_chatbot_nlp = nlp(mensagem_chatbot)

                    procedimento_verbs = " ".join([token.lemma_ for token in procedimento_nlp if token.pos_ == "VERB"])
                    procedimento_ajds = " ".join([token.lemma_ for token in procedimento_nlp if token.pos_ == "ADJ"])
                    procedimento_nouns = " ".join([token.lemma_ for token in procedimento_nlp if token.pos_ == "NOUN"])
        
                    mensagem_chatbot_verbs = " ".join([token.lemma_ for token in mensagem_chatbot_nlp if token.pos_ == "VERB"])
                    mensagem_chatbot_ajds = " ".join([token.lemma_ for token in mensagem_chatbot_nlp if token.pos_ == "ADJ"])
                    mensagem_chatbot_nouns = " ".join([token.lemma_ for token in mensagem_chatbot_nlp if token.pos_ == "NOUN"])
        
                    nota_resposta_individual.append(( # Calcula a média das comparações de adjetivos, verbos e substantivos de cada mensagem e procedimento 
                        nlp(procedimento_verbs)
                        .similarity(nlp(mensagem_chatbot_verbs)) + 
                        nlp(procedimento_ajds)
                        .similarity(nlp(mensagem_chatbot_ajds)) + 
                        nlp(procedimento_nouns)
                        .similarity(nlp(mensagem_chatbot_nouns))
                        ) / 3 * 5
                    )
                nota_resposta.append(statistics.mean(nota_resposta_individual))
                mensagem_chatbot = None
    #Tratar as notas para que fiquem em um espaço de 0 a 5
    return statistics.mean(nota_tema), statistics.mean(nota_resposta)


jsonTest = {
  "setor": "detran",
  "area": "habilitação",
  "serviço": "renovar a carteira",
  "etapas": {
    "1": "Preencher formulário de solicitação",
    "2": "Agendar exame médico",
    "3": "Realizar exame psicotécnico",
    "4": "Efetuar pagamento da taxa de renovação",
    "5": "Retirar nova carteira de habilitação"
  },
  "fonte": "https://endereçopublico.com/lasdjfalsdf"
}
for nome_arquivo in os.listdir("conversation"):
    nota1, nota2 = testConversation("Renovação CNH", jsonTest, "conversation/" + nome_arquivo)
    print(nota1, nota2)