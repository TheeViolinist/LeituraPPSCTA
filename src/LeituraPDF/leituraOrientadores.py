import PyPDF2
#from PyPDF2.pdf import PageObject
import re
import json
from unidecode import unidecode

#Codigo responsável pela leitura de um arquivo com os dados de orientadores e suas áreas
#Do PDF responsável pelo enic daquele ano e cria um arquivo de dados contendo os resumos de cada orientador junto as suas áreas e subáreas



quantidadeResumos =  96 # Variável que irá ser responsável por percorrer todas as páginas que possuem resumo
resumos: list = []  # Lista onde ficará armazenado os dicionários sobre cada resumo


nome_pdf = "../DadosEnic/enic16.pdf"
resumo_nome = "../resumoOrientadores/resumoOrientadores16.json"
caminho_projetos = "../CriadorDadosModelo/projetos2016.json"
planos_nao_achados = "../resumoOrientadores/nao_achados16.txt"

      

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




#Estamos abrindo um arquivo para leitura binária, nomeado de resumo
with open(nome_pdf, 'rb') as resumo_pdf:
    # Fazendo a leitura do documento e armazenando em um objeto chamado resumoRead
    resumoRead = PyPDF2.PdfReader(resumo_pdf)

    # Pega-se o número de páginas e armazenar em um objeto chamado resumoPages
    resumoPages = len(resumoRead.pages)
    
    # Nome do resumo a ser criado
    projetos = abre_projetos(caminho_projetos)
    
    # Cria lista de projetos que foram achados ou não, inicaliza todas as variáveis como False
    achados = 0
    projetos_contidos = list()
    

    for i in range(len(projetos)):
        projetos_contidos.append(False)


    while quantidadeResumos < resumoPages:
        print(quantidadeResumos)

        # Vamos ler a página dada como parâmetro e armazenar em um objeto chamado page

        page = resumoRead.pages[quantidadeResumos]

        # Extraimos o texto daquele objeto extraido na linha anterior

        pageConteudo = page.extract_text()


        
        # Vamos retirar a quebra de linhas
        pageConteudo = re.sub('\n', '', pageConteudo)
        page_sem_espaco = re.sub(' ', '',pageConteudo)
        
        
        projeto_achado = False
        indice_projeto_achado = 0
        
        
        indice = 0 # Indice do projeto
        for projeto in projetos:
            
            projeto_plano = re.sub(' ', '', projeto['Plano:'])

            if unidecode(projeto_plano) in unidecode(page_sem_espaco):
                projeto_achado = True #Diz se o projeto foi achado ou não
                achados += 1    #Ver quantos foram achados
                projetos_contidos[indice] = True
                indice_projeto_achado = indice

            indice += 1
            
              
        
       
        if(projeto_achado) :
            posicaoResumoInicial: int = 0
            #Vamos pegar a posição do início do resumo daquela página
            if pageConteudo.find("Resumo:") != - 1:
                posicaoResumoInicial = pageConteudo.find("Resumo:")
            else:
               posicaoResumoInicial = pageConteudo.find("RESUMO") - 1

            #Posicao Final do resumo é quando achamos a string "Palavras-Chave:"
            
            posicaoResumoFinal: int = 0
            if pageConteudo.find("Palavras-Chave:") != -1:
                posicaoResumoFinal = pageConteudo.find("Palavras-Chave:")
            elif pageConteudo.find("Palav ras-Chave") != -1:
                posicaoResumoFinal = pageConteudo.find("Palav ras-Chave")
            elif pageConteudo.find("Palavras Chave") != -1:
                posicaoResumoFinal = pageConteudo.find("Palavras Chave")
            else:
                posicaoResumoFinal = pageConteudo.find("Palavras -Chave")

        
            #Recebe-se o dicionário
            resumo_dict = projetos[indice_projeto_achado]
            resumo_dict['texto:'] = pageConteudo[posicaoResumoInicial + 8:posicaoResumoFinal].lstrip()
            resumo_dict['texto:'] = resumo_dict["texto:"].rstrip()
            
            #Adiciona-se o dicionario na lista de resumos
            resumos.append(resumo_dict.copy())
        
        quantidadeResumos += 1      # Aumenta-se em um a variável de controle do loop

    # Responsável por criar o json do resumo dos orientadores
    with open(resumo_nome, 'w') as resumo_js:
        json.dump(resumos, resumo_js, indent = 4, ensure_ascii=False)
    resumo_js.close()
    
    # Cria um arquivo txt responsável por dizer quais foram os planos não achados
    arq_nao_achados = open(planos_nao_achados, "w+")

    for i in range(len(projetos_contidos)):
        if projetos_contidos[i] == False:
            arq_nao_achados.write(projetos[i]['Plano:'])
            arq_nao_achados.write('\n')
    arq_nao_achados.close()

    
    print(f'Foram achados {len(resumos)} resumos')
    
    resumo_pdf.close()
    
    

    


















