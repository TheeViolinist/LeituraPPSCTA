import PyPDF2
#from PyPDF2.pdf import PageObject
import re
import json
from unidecode import unidecode

#Codigo responsável pela leitura de um arquivo com os dados de orientadores e suas áreas
#Do PDF responsável pelo enic daquele ano e cria um arquivo de dados contendo os resumos de cada orientador junto as suas áreas e subáreas



quantidadeResumos =  94 # Variável que irá ser responsável por percorrer todas as páginas que possuem resumo
indiceResumo = 0 # Indice de Resumo que indica que trabalho é aquele
resumos: list = []  # Lista onde ficará armazenado os dicionários sobre cada resumo
no_read: int = 0   # Variável para poder encontrar alguma não leitura do pdf
orientadores_achados: int = 0
quantia_nao_achados: int = 0

nome_pdf = "../DadosEnic/enic14.pdf"
resumo_nome = "../resumoOrientadores/cdresumoOrientadores14.json"
nome_orientadores = "../CriadorDados/projetos2014.json"






        

# Função responsável por retirar o email do nome
# No Enic 17 foi necessário essa mudança, pois o algoritmo atual armazenava o email junto a string do nome
def retira_email(nome_e_email):

    frase: str= nome_e_email

    palavras: list = frase.split()

    palavra_final: str = ""

    for palavra in palavras:
        palavra_final += (palavra if '@' not in palavra else '') + ' '

    

    return palavra_final

 

# Função responsável por escrever o texto inteiro em um arquivo 
def escreve_texto(indice, nome_orientador, dados_orientador):
    
    # Criação de um dicionário
    resumo:dict = {}
    # Armazena-se nas chaves indice, titulo e texto todo o conteudo do resumo e retora-se esse dicionario
    resumo["indice"] = indice
    resumo["orientador"] = dados_orientador["nome"]
    resumo["area"] = dados_orientador["area"]
    resumo["subarea"] = dados_orientador["subarea"]
    #Printa-se tudo que está após resumo, utilizamos posicaoResumoInicial + 8, pois 8 é o tamanho da string resumo e queremos iniciar após ela
    #Logo, termina quando achar a string "Palavras-Chave: que está no índice posicaoResumoFinal"
    resumo["texto"] = pageConteudo[posicaoResumoInicial + 8:posicaoResumoFinal].lstrip()
    resumo["texto"] = resumo["texto"].rstrip()

    
    return resumo



def abre_orientadores(orientadores_arquivo):
    
    orientadores = list()
    with open(orientadores_arquivo) as file:
        orientadores = json.load(file)
    file.close()
    return orientadores


def retorna_orientador_page(page):
    
    page = page.lower()
    posicaoInicial = page.find('e-mail') + 6
    posicaoFinal = page.find("orientador")
    nome_total = str()
    nome_total = page[posicaoInicial:posicaoFinal]
    
    #Processo de tratamento, vamos retirar os espaços entre os nomes
    # Tratatei o nome até a primeira letra
    for letra in nome_total:
        if(letra == ')'):
            nome_total = nome_total.replace(letra, '', 1)
            break
        nome_total = nome_total.replace(letra, '', 1)
    
    nome_total = nome_total.rstrip()
    nome_total = nome_total.lstrip()


   
    # Retira todos os espaços em branco dubplo
    nome_total = " ".join(re.split(r"\s+", nome_total))

    # Ano 2014 vamos pegar apenas os dois primeiros nomes
    nome = list()
    nome_total = unidecode.unidecode(nome_total) # retira os caracteres especiais do nome
    nome_total_separado = nome_total.split(' ')
    
    #Retira todos as letras sepradas
    for name in nome_total_separado:
        if len(name) == 1:
            continue
        nome.append(name.upper())

    
    return nome


#Estamos abrindo um arquivo para leitura binária, nomeado de resumo
with open(nome_pdf, 'rb') as resumo_pdf:
    # Fazendo a leitura do documento e armazenando em um objeto chamado resumoRead
    resumoRead = PyPDF2.PdfReader(resumo_pdf)

    # Pega-se o número de páginas e armazenar em um objeto chamado resumoPages
    resumoPages = len(resumoRead.pages)
    
    # Nome do resumo a ser criado
    projetos = abre_orientadores(nome_orientadores)

    achados = 0

    while quantidadeResumos < resumoPages:
        print(quantidadeResumos)

        # Vamos ler a página dada como parâmetro e armazenar em um objeto chamado page

        page = resumoRead.pages[quantidadeResumos]

        # Extraimos o texto daquele objeto extraido na linha anterior

        pageConteudo = page.extract_text()


        
        # Vamos retirar a quebra de linhas
        pageConteudo = re.sub('\n', '', pageConteudo)
        page_sem_espaco = re.sub(' ', '',pageConteudo)
        
        
        projeto_contido = False
        

        for projeto in projetos:
            projeto_plano = re.sub(' ', '', projeto['Plano:'])
    
            if unidecode(projeto_plano) in unidecode(page_sem_espaco):
                projeto_contido = True
                achados += 1
        
        if(projeto_contido == False):
            print(pageConteudo)
            a = input()
                
        
       
        #if(1) :
         #   posicaoResumoInicial: int = 0
            #Vamos pegar a posição do início do resumo daquela página
          #  if pageConteudo.find("Resumo:") != - 1:
           #     posicaoResumoInicial = pageConteudo.find("Resumo:")
            #else:
             #   posicaoResumoInicial = pageConteudo.find("RESUMO") - 1

            #Posicao Final do resumo é quando achamos a string "Palavras-Chave:"
            #posicaoResumoFinal  = pageConteudo.find("Palavras-Chave:")
        
            #Recebe-se o dicionário
            #resumo_dict: dict
            #resumo_dict: dict= escreve_texto(indiceResumo, orientador_nome, orientadores[indiceOrientadorAchado])
            #Adiciona-se o dicionario na lista de resumos
            #resumos.append(resumo_dict.copy())
        
        quantidadeResumos += 1      # Aumenta-se em um a variável de controle do loop
        #indiceResumo += 1           # Aumenta-se em um o índice do resumo
        #nomeTrabalho = ''                   # Limpa-se o nome do trabalho

    #with open(resumo_nome, 'w') as resumo_js:
    #    json.dump(resumos, resumo_js, indent = 4, ensure_ascii=False)
    #resumo_js.close()
    
    print(achados)
    print(no_read)
    print(orientadores_achados)
    print(quantia_nao_achados)
    resumo_pdf.close()
    
    

    


















