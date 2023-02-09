import PyPDF2
from PyPDF2.pdf import PageObject
import re
import json

quantidadeResumos =  104 # Variável que irá ser responsável por percorrer todas as páginas que possuem resumo
indiceResumo = 0 # Indice de Resumo que indica que trabalho é aquele
resumos: list = []  # Lista onde ficará armazenado os dicionários sobre cada resumo
no_read: int = 0   # Variável para poder encontrar alguma não leitura do pdf
orientadores_achados: int = 0


#ome_pdf: str = input() # Nome do pdf que será lido
#resumo_nome: str = input() # Nome do resumo para criar o arquivo
#arquivo_alunos: str = input() # nome do arquivos de alunos para ler
#nome_orientadores: str = input()

nome_pdf = "DadosEnic/enic17.pdf"
resumo_nome = "resumoOrientadores17.json"
nome_orientadores = "DadosOrientadores/orientadores2017Areas.txt"





        

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
    resumo["texto"] = pageConteudo[posicaoResumoInicial + 8:posicaoResumoFinal]

    
    return resumo



def abre_orientadores(orientadores_arquivo):
    arq = open(orientadores_arquivo, 'r')

    orientadores = dict()
    linhas = arq.readlines()
    orientadores_dados = list()
    orientadores_dictionary_list = list()
    indice = 0
    while(indice < len(linhas)):

        orientadores["nome"] = linhas[indice]
        orientadores_dados = linhas[indice + 1].split(' ', 1)
        orientadores["area"] = orientadores_dados[0]
        orientadores["subarea"] = orientadores_dados[1]
        orientadores_dictionary_list.append(orientadores.copy())
        indice += 2
            
        
    
    return orientadores_dictionary_list



#Estamos abrindo um arquivo para leitura binária, nomeado de resumo
with open(nome_pdf, 'rb') as resumo_pdf:
    # Fazendo a leitura do documento e armazenando em um objeto chamado resumoRead
    resumoRead = PyPDF2.PdfFileReader(resumo_pdf)

    # Pega-se o número de páginas e armazenar em um objeto chamado resumoPages
    resumoPages = resumoRead.getNumPages()
    # Nome do resumo a ser criado
  


    while quantidadeResumos < resumoPages:
        

        # Vamos ler a página dada como parâmetro e armazenar em um objeto chamado page

        page:PageObject = resumoRead.getPage(quantidadeResumos)

        # Extraimos o texto daquele objeto extraido na linha anterior

        pageConteudo = page.extractText()


        
        # Vamos retirar a quebra de linhas
        pageConteudo = re.sub('\n', '', pageConteudo)
       

        
        # Primeiramente temos que retirar o nome dos autores do arquivo de texto
        # Fazemos isso chamando a função nome_alunos o qual retorna uma lista contendo os nomes
        #nome_autores:list = nome_alunos(arquivo_alunos)
        
        orientadores = abre_orientadores(nome_orientadores)
        


        
        achou = False
        orientador_nome = str()
        indiceOrientadorAchador = 0

        for orientador in orientadores:
            
            orientador_nome_procurar = orientador["nome"].replace('\n', '')
            if(pageConteudo.find(orientador_nome_procurar) != -1) :
                orientador_nome = orientador
                achou = True
                orientadores_achados += 1
                break
            
            indiceOrientadorAchador += 1
        
       
        if(achou) :
            posicaoResumoInicial: int = 0
            #Vamos pegar a posição do início do resumo daquela página
            if pageConteudo.find("Resumo:") != - 1:
                posicaoResumoInicial = pageConteudo.find("Resumo:")
            else:
                posicaoResumoInicial = pageConteudo.find("RESUMO") - 1

            #Posicao Final do resumo é quando achamos a string "Palavras-Chave:"
            posicaoResumoFinal  = pageConteudo.find("Palavras-Chave:")
        
            #Recebe-se o dicionário
            resumo_dict: dict= escreve_texto(indiceResumo, orientador_nome, orientadores[indiceOrientadorAchador])
            #Adiciona-se o dicionario na lista de resumos
            resumos.append(resumo_dict.copy())
        
        quantidadeResumos += 1      # Aumenta-se em um a variável de controle do loop
        indiceResumo += 1           # Aumenta-se em um o índice do resumo
        nomeTrabalho = ''                   # Limpa-se o nome do trabalho

    with open(resumo_nome, 'w') as resumo_js:
        json.dump(resumos, resumo_js, indent = 4, ensure_ascii=False)
    resumo_js.close()
   
    print(no_read)
    print(orientadores_achados)
    resumo_pdf.close()
    
    

    


















