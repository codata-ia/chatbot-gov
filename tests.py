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
                nota_tema.append(fuzz.token_set_ratio(mensagem_chatbot, tema) / 100) #Usar fuzz para calcular sobre o tema token_set_ratio
                
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
                        ) / 3
                    )
                nota_resposta.append(statistics.mean(nota_resposta_individual))
                mensagem_chatbot = None
    #Tratar as notas para que fiquem em um espaço de 0 a 5
    return statistics.mean(nota_tema), statistics.mean(nota_resposta)


servicos_json = [
    {
        "servico": "Renovação CNH",
        "etapas": {
            1: "Acesse o 'Portal de Serviços' no link, https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app e crie sua conta (fique atento ao código que será enviado por e-mail para validar seu cadastro e criar senha de acesso);",
            2: "No seu cadastro, coluna de serviços, no link, https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app, selecione Habilitação, Serviços, S21-EMISSÃO DE BOLETOS CNH, emita a guia de RENOVAÇÃO CNH. ATENÇÃO: Pague e guarde o boleto (irá precisar do número do boleto pago – nosso número – para marcar todos os exames). Em até 24 horas o boleto é compensado",
            3: "Acesse S18-SOLICITAR RENOVAÇÃO CNH no link, https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app , preencha os dados, gere e emita o seu Comprovante de Renovação - RENACH. OBSERVAÇÃO: Nessa opção será possível escolher o local de recebimento da sua CNH",
            4: "Acesse a página de agendamentos, no link, https://wsdetran.pb.gov.br/detran-agendamento/inicio, selecione “Habilitação”, siga para agendar “Captura ONLINE (Foto e Biometria presencial)”. Salve o agendamento ou imprima e compareça no local, data e horário agendado com os seguintes documentos indicados no respectivo agendamento;",
            5: "USE ESSA OPÇÃO APENAS SE EXERCER ATIVIDADE REMUNERADA (EAR) - Na opção S25- AGENDAMENTO DE EXAME PSICOTÉCNICO no link, https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app  com CPF e número da guia de renovação (nosso número) e compareça no local, data e horário agendado, levando o comprovante de agendamento e documento oficial com foto (o exame é pago à clínica no dia do exame)",
            6: "Na opção S17-AGENDAMENTO DE EXAME MÉDICO, no link, https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app, agende seu exame médico (de vista) com CPF e número da guia de renovação (nosso número) e compareça no local, data e horário agendado, levando o comprovante de agendamento e documento oficial com foto (exame e pago à clínica no dia do exame)",
            7: "Após apto em todos os exames, acompanhe a confirmação da emissão da CNH no link, https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app, na opção S35- CONSULTAR SITUAÇÃO DA CNH. Quando a “Situação da CNH” estiver “CONFIRMADA EMISSÃO”, acesse a página de agendamentos - https://wsdetran.pb.gov.br/detran-agendamento/inicio - , “Habilitação” e agende “Recebimento de Habilitação (CNH Impressa)”. Salve o agendamento ou imprima e compareça no local, data e horário agendado com os seguintes documentos indicados no respectivo agendamento."
        },
        "fonte": "https://detran.pb.gov.br/habilitacao-1/renovacao-cnh"
    },
    {
        "servico": "Licenciamento - Emissão de boleto bancário e consulta",
        "etapas": {
            1: "Acessar o site do DETRAN em: www.detran.pb.gov.br",
            2: "Clicar em: Licenciamento;",
            3: "Informar: placa, CPF, ano do licenciamento;",
            4: "Selecionar: Emitir guia de pagamento (Boleto Bancário), depois clicar em: Enviar",
            5: "Será gerada em PDF uma guia de recolhimento, que deve ser efetuada o pagamento no Banco do Brasil, no aplicativo do BB ou no Pague Fácil;",
            6: "Retorne ao site do DETRAN, para gerar em PDF a guia de recolhimento do IPVA;",
            7: "Clique no link: IPVA para saber quais os procedimentos para gerar a guia de recolhimento.",
            8: "Após pagamento acessar o site do Detran, clique no link Emitir CRLV Digital ou agendar para receber no Detran."
        },
        "fonte": "https://detran.pb.gov.br/formularios/licenciamento"
    },
    {
        "servico": "Comunicação de Venda",
        "etapas": {
            1: "Acesse o Portal de Serviços do DETRAN-PB, e siga os passos para realizar o cadastro(se não possuir), colocando o número do CPF e e-mail válido. Receberá um código por e-mail para validar seu cadastro e criar senha de acesso;",
            2: "Acesse o portal com CPF e senha, em seguida selecione a opção Veículos(menu lateral) , depois COMUNICAÇÃO DE VENDA e preencha os dados solicitados;",
            3: "Após o requerimento de comunicação de venda, é necessário aguardar a análise da solicitação, o usuário receberá por e-mail o resultado da avaliação. Se o requerimento for DEFERIDO, a comunicação de venda será registrada no sistema. Se o requerimento for INDEFERIDO, será encaminhado e-mail indicando os motivos do indeferimento orientando o usuário como proceder."
        },
        "fonte": "https://detran.pb.gov.br/veiculos/comunicacao-de-venda"
    },
    {
        "servico": "Emissão de ATPV",
        "etapas": {
            1: "Acesse o Portal de Serviços do DETRAN-PB, e siga os passos para realizar o cadastro(se não possuir), colocando o número do CPF e e-mail válido. Receberá um código por e-mail para validar seu cadastro e criar senha de acesso;",
            2: "Acesse o portal com CPF e senha, em seguida selecione a opção Veículos(menu lateral) , depois REGISTRAR INTENÇÃO DE VENDA(ATPV) e preencha os dados solicitados;",
            3: "Após o preenchimento, o proprietário deverá imprimir o PDF e reconhecer as assinaturas(vendedor e comprador) por autenticidade;",
            4: "Na sequência, a ATPV e demais documentos exigidos deverão ser apresentados ao DETRAN para transferência."
        },
        "fonte": "https://detran.pb.gov.br/veiculos/emissao-de-atpv"
    },
    {
        "servico": "Cancelar ATPV",
        "etapas": {
            1: "Acesse o Portal de Serviços do DETRAN-PB, e siga os passos para realizar o cadastro(se não possuir), colocando o número do CPF e e-mail válido. Receberá um código por e-mail para validar seu cadastro e criar senha de acesso;",
            2: "Acesse o portal com CPF/CNPJ e senha, em seguida selecione a opção Veículos(menu lateral) , depois CANCELAR INTENÇÃO DE VENDA(ATPV) e preencha os dados solicitados;",
            3: "Após o preenchimento dos dados solicitados, o sistema apresenta uma opção para emitir boleto, após efetuar o pagamento, aguardar no mínimo 30 minutos, deverá deverá acessar o sistema, opção CANCELAR INTENÇÃO DE VENDA(ATPV), informar os dados solicitados, se o pagamento estiver sido realizado o sistema vai apresentar a opção 'Confirmar Cancelamento de ATPV', feito isso o veículo está liberado para registrar uma nova intenção de venda."
        },
        "fonte": "https://detran.pb.gov.br/veiculos/cancelar-atpv"
    },{
        "servico": "Primeiro Emplacamento (0km)",
        "etapas": {
            1: "Acesse o site da SEFAZ-PB em: https://www.sefaz.pb.gov.br/servirtual/ipva/emitir-dar-primeiro-emplacamento e emita a guia de pagamento do IPVA primeiro emplacamento - SER/PB. Efetue o pagamento da guia referente ao IPVA. Aguarde a compensação bancária (aproximadamente 40 minutos).",
            2: "Acesse o Portal de Serviços do DETRAN-PB em: https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app?op=S38 para cadastrar/acessar o Portal de Serviços do DETRAN-PB, utilizando CPF/CNPJ e senha do proprietário do veículo. Acesse o serviço S38 - PRIMEIRO EMPLACAMENTO ON-LINE (0KM), localizado no menu Veículos. Preencha os dados solicitados conforme a Nota Fiscal do veículo e, ao final, emita a guia de pagamento do Primeiro Emplacamento. Efetue o pagamento. Guarde uma cópia da guia de pagamento (digital ou impressa).",
            3: "Acesse o Portal de Serviços do DETRAN-PB em: https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app?op=S11 para acessar o serviço de consulta de andamento de processo do DETRAN-PB. Preencha as informações solicitadas (número do processo e a placa) e clique em Consultar. Essas informações podem ser encontradas na guia de pagamento do Emplacamento. Preencha os dados solicitados conforme a Nota Fiscal do veículo e, ao final, emita a guia de pagamento do Primeiro Emplacamento. Quando o sistema mostrar a mensagem 'COMPARECER AO ESTAMPADOR PARA COLOCAÇÃO DA PLACA', o proprietário deve emitir o documento do veículo, conforme descrito abaixo.",
            4: "Acesse o site do DETRAN-PB em: https://wsdetran.pb.gov.br/detran-agendamento/inicio para agendar o serviço de instalação de Placa para a unidade do Detran escolhida no início deste processo. Na concessionária, procure a concessionária para agendamento da instalação da placa.",
            5: "Acesse o Portal de Serviços do DETRAN-PB em: https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app?op=S39 para acessar o Portal de Serviços do DETRAN-PB, utilizando CPF/CNPJ e senha do proprietário do veículo. Acesse o serviço S39 - EMITIR CRV (PRIMEIRO EMPLACAMENTO 0KM), localizado no menu Veículos. Preencha as informações solicitadas (número do processo e a placa) conforme encontradas na guia de pagamento do Emplacamento. Realize a emissão do CRV e CRLV do veículo."
        },
        "fonte": "https://detran.pb.gov.br/veiculos/primeiro-emplacamento-0km"
    },
    {
        "servico": "Habilitação Definitiva",
        "etapas": {
            1: "Acesse o Portal de Serviços no link: https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app e crie sua conta (fique atento ao código que será enviado por e-mail para validar seu cadastro e criar senha de acesso);",
            2: "No seu cadastro, na coluna de serviços, acesse o link: https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app, selecione Habilitação, Serviços, S21-EMISSÃO DE BOLETOS CNH, emita a guia de CNH DEFINITIVA. ATENÇÃO: Pague e guarde o boleto (irá precisar do número do boleto pago – nosso número – para marcar todos os exames). Em até 24 horas o boleto é compensado;",
            3: "No portal de serviços no link: https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app, acesse S14 – SOLICITAR CNH 2ª VIA /DEFINITIVA, preencha os dados solicitados e finalize confirmando o pedido de emissão. OBSERVAÇÃO: Nessa opção será possível escolher o local de recebimento da sua CNH;",
            4: "Acompanhe a confirmação da emissão da CNH no link: https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app, na opção S35-CONSULTAR SITUAÇÃO DA CNH. Quando a “Situação da CNH” estiver “CONFIRMADA EMISSÃO”, acesse a página de agendamentos - https://wsdetran.pb.gov.br/detran-agendamento/inicio -, “Habilitação” e agende “Recebimento de Habilitação (CNH Impressa)”. Salve o agendamento ou imprima e compareça no local, data e horário agendado com os seguintes documentos indicados no respectivo agendamento."
        },
        "fonte": "https://detran.pb.gov.br/habilitacao-1/habilitacao-definitiva"
    },
    {
        "servico": "Segunda Via CNH",
        "etapas": {
            1: "Acesse o Portal de Serviços no link: https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app e crie sua conta (fique atento ao código que será enviado por e-mail para validar seu cadastro e criar senha de acesso);",
            2: "No seu cadastro, na coluna de serviços, acesse o link: https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app, selecione Habilitação, Serviços, S21-EMISSÃO DE BOLETOS CNH, emita a guia de 2ª via de CNH. ATENÇÃO: Pague e guarde o boleto (irá precisar do número do boleto pago – nosso número – para marcar todos os exames). Em até 24 horas o boleto é compensado;",
            3: "No portal de serviços no link: https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app, acesse S14 – SOLICITAR CNH 2ª VIA /DEFINITIVA, preencha os dados solicitados e finalize confirmando o pedido de emissão. OBSERVAÇÃO: Nessa opção será possível escolher o local de recebimento da sua CNH;",
            4: "Acompanhe a confirmação da emissão da CNH no link: https://wsdetran.pb.gov.br/detran-portal-servicos/servlet/easynat-app, na opção S35-CONSULTAR SITUAÇÃO DA CNH. Quando a “Situação da CNH” estiver “CONFIRMADA EMISSÃO”, acesse a página de agendamentos - https://wsdetran.pb.gov.br/detran-agendamento/inicio -, “Habilitação” e agende “Recebimento de Habilitação (CNH Impressa)”. Salve o agendamento ou imprima e compareça no local, data e horário agendado com os seguintes documentos indicados no respectivo agendamento."
        },
        "fonte": "https://detran.pb.gov.br/habilitacao-1/segunda-via-cnh"
    }
]

for nome_arquivo in os.listdir("conversation"):
    for servico in servicos_json:
        nota1, nota2 = testConversation(servico["servico"], servico, "conversation/" + nome_arquivo)
        print(f"nota tema: {nota1}, nota resposta: {nota2}, arquivo: {nome_arquivo}, serviço: {servico["servico"]}")