

import fitz  # PyMuPDF
import re
import json
from unidecode import unidecode

#Codigo responsável pela leitura de um arquivo com os dados de orientadores e suas áreas
#Do PDF responsável pelo enic daquele ano e cria um arquivo de dados contendo os resumos de cada orientador junto as suas áreas e subáreas


# A pagina inicial deve ser a pagina do pdf que começam os resumos -1
quantidadeResumos =  103 # Variável que irá ser responsável por percorrer todas as páginas que possuem resumo
resumos: list = []  # Lista onde ficará armazenado os dicionários sobre cada resumo


nome_pdf = "../DadosEnic/enic17.pdf"
resumo_nome = "../resumoOrientadores/resumoOrientadores17.json"
caminho_projetos = "../CriadorDadosModelo/projetos2017.json"
planos_nao_achados = "../resumoOrientadores/nao_achados17.txt"

      

# Função responsável por retirar o email do nome
# No Enic 17 foi necessário essa mudança, pois o algoritmo atual armazenava o email junto a string do nome
def retira_email(nome_e_email):

    frase: str= nome_e_email

    palavras: list = frase.split()

    palavra_final: str = ""

    for palavra in palavras:
        palavra_final += (palavra if '@' not in palavra else '') + ' '

    

    return palavra_final


#Abre o arquivo json de projetos
def abre_projetos(projetos_arquivo):
    
    projetos = list()
    with open(projetos_arquivo) as file:
        projetos = json.load(file)
    file.close()
    return projetos


def clean_text(text):
    # Substituir múltiplos espaços por um único espaço
    text = re.sub(r'\s+', ' ', text)
    
    # Remover caracteres especiais e não-ASCII
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # Remover quebras de linha e tabulações
    text = text.replace('\n', ' ').replace('\t', ' ')
    
    # Remover espaços em branco extras no início e no final
    text = text.strip()
    
    return text



#Função responsável por receber uma string e retornar apenas em formato asc
def asc_string(string):

    text = ''
    for letter in string:
        if ord(letter) <= 122 and ord(letter) >= 97:
            text += letter

    return text


#Estamos abrindo um arquivo para leitura binária, nomeado de resumo
with open(nome_pdf, 'rb') as resumo_pdf:
    # Fazendo a leitura do documento e armazenando em um objeto chamado resumoRead
    resumoRead = fitz.open(stream=resumo_pdf.read(), filetype="pdf")


    # Pega-se o número de páginas e armazenar em um objeto chamado resumoPages
    resumoPages = resumoRead.page_count
    
    # Nome do resumo a ser criado
    projetos = abre_projetos(caminho_projetos)
    
    # Cria lista de projetos que foram achados ou não, inicaliza todas as variáveis como False
    achados = 0
    projetos_contidos = list()
    

    for i in range(len(projetos)):
        projetos_contidos.append(False)


    enic_resumos = list()
    enic_resumos_sem_espaco = list()
    while quantidadeResumos < resumoPages:
        print(quantidadeResumos)
        
            
        # Vamos ler a página dada como parâmetro e armazenar em um objeto chamado page

        page = resumoRead.load_page(quantidadeResumos)

        # Extraimos o texto daquele objeto extraido na linha anterior

        pageConteudo = page.get_text("text")
        pageConteudo = re.sub('\n', '', pageConteudo)
        
        # Lista para retirar os resumos
        enic_resumos.append(pageConteudo)


        # Tratamento para localizar o plano
        # Pois algumas instancias do ENIC bugava com letras não ascii
        page_sem_espaco = (re.sub(' ', '', pageConteudo)).lower()
        page_sem_espaco = asc_string(page_sem_espaco)
        enic_resumos_sem_espaco.append(page_sem_espaco)
  
        
        quantidadeResumos += 1
        
    print("Lido todo o PDF")

    for i, projeto in enumerate(projetos):
        # Realiza o tratamento do texto para o nome do plano
        projeto_plano = re.sub('\n', '', projeto['Plano:'])
        projeto_plano = re.sub(' ', '', projeto_plano)
        text_treated = asc_string(projeto_plano.lower())
        
        
        projeto_achado = False
        indice_projeto_achado = 0
        
        for j, page in enumerate(enic_resumos):

           
    
            if enic_resumos_sem_espaco[j].find(text_treated):
                projeto_achado = True
                achados += 1
                projetos_contidos[i] = True
                indice_projeto_achado = i
                
            if(projeto_achado) :
                posicaoResumoInicial: int = 0
                #Vamos pegar a posição do início do resumo daquela página
                if page.find("Resumo:") != - 1:
                    posicaoResumoInicial = page.find("Resumo:")
                else:
                    posicaoResumoInicial = page.find("RESUMO") - 1

                #Posicao Final do resumo é quando achamos a string "Palavras-Chave:"
                
                posicaoResumoFinal: int = 0
                if pageConteudo.find("Palavras-Chave:") != -1:
                    posicaoResumoFinal = page.find("Palavras-Chave:")
                elif pageConteudo.find("Palav ras-Chave") != -1:
                    posicaoResumoFinal = page.find("Palav ras-Chave")
                elif pageConteudo.find("Palavras Chave") != -1:
                    posicaoResumoFinal = page.find("Palavras Chave")
                else:
                    posicaoResumoFinal = page.find("Palavras -Chave")

            
                #Recebe-se o dicionário
                resumo_dict = projetos[indice_projeto_achado]
                resumo_dict['texto:'] = page[posicaoResumoInicial + 8:posicaoResumoFinal].lstrip()
                resumo_dict['texto:'] = resumo_dict["texto:"].rstrip()
                
                incluso = False
                for resumo in resumos:
                    if resumo["id"] == resumo_dict["id"]:
                        incluso = True
                        
                if not incluso:
                    #Adiciona-se o dicionario na lista de resumos
                    resumos.append(resumo_dict.copy())
                break
            
       

    
    # Responsável por criar o json do resumo dos orientadores
    with open(resumo_nome, 'w') as resumo_js:
        json.dump(resumos, resumo_js, indent = 4, ensure_ascii=False)
    resumo_js.close()
    
    # Cria um arquivo txt responsável por dizer quais foram os planos não achados
    arq_nao_achados = open(planos_nao_achados, "w+")

    for i in range(len(projetos_contidos)):
        if projetos_contidos[i] == False:
            arq_nao_achados.write(str(i) + ' ')
            arq_nao_achados.write('\n')
            
    arq_nao_achados.close()

    
    print(f'Foram achados {len(resumos)} resumos')
    
    resumo_pdf.close()
    
    

    


















