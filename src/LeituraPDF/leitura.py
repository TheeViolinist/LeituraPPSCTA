import PyPDF2
from PyPDF2.pdf import PageObject
import re
import json

quantidadeResumos =  93 # Variável que irá ser responsável por percorrer todas as páginas que possuem resumo
indiceResumo = 0 # Indice de Resumo que indica que trabalho é aquele
resumos: list = []  # Lista onde ficará armazenado os dicionários sobre cada resumo
no_read: int = 0   # Variável para poder encontrar alguma não leitura do pdf



nome_pdf: str = input() # Nome do pdf que será lido
resumo_nome: str = input() # Nome do resumo para criar o arquivo
arquivo_alunos: str = input() # nome do arquivos de alunos para ler
nome_orientadores: str = input()




# Função responsável por retirar o nome dos alunos do arquivo
def nome_alunos(arquivo_alunos: str):
    nomes_dos_alunos:list = []

    with open(arquivo_alunos, "r") as alunos:
        for line in alunos:
            # Armazena-se temporareamente aquela linha em outra string
            nome = line
            # Retira-se a quebra de linha
            nome = nome.replace("\n", "")
            # Adiciona o nome do autor a lista de nome de autores
            nomes_dos_alunos.append(nome)

    

    alunos.close()
    
    # Retorna-se a lista de alunos
    return nomes_dos_alunos
    

        

# Função responsável por retirar o nome do trabalho junto ao nome do autor
def retira_trabalho_autor():
    # Posicao inicial de onde começa o nome do trabalho
    if(pageConteudo.find("Bananeiras-PB") != -1):
        posicao_inicial_trabalho = pageConteudo.find("Bananeiras-PB") + 14
    # dependendo da instancia do enic, devemos mudar essa string
    elif(pageConteudo.find("XXV ENCONTRO DE INICIAÇÃO CIENTÍFICA") != -1):
        posicao_inicial_trabalho = pageConteudo.find("XXV ENCONTRO DE INICIAÇÃO CIENTÍFICA") + 37
        
   

    # Cria-se uma nova string que começa da posição inicial do trabalho
    nome: str = pageConteudo[posicao_inicial_trabalho:]
    

  

    # Pega-se a posição final da linha que contém o nome do trabalho e o nome do autor
    # Cada if refere-se a uma instancia do enic diferente
    if(nome.find("Autor(a)") != -1):
        posicao_final_trabalho = nome.find("Autor(a)")
    elif(nome.find("- Aluno") != -1):
        posicao_final_trabalho = nome.find("- Aluno")
    elif(nome.find("Programa") != -1):
        posicao_final_trabalho = nome.find("Programa") - 2
    elif(nome.find("PIVIC") != -1):
        posicao_final_trabalho = nome.find("- PIVIC ") - 19
    elif(nome.find(" PIBIC") != -1):
        posicao_final_trabalho = nome.find("- PIBIC") - 19
    elif(nome.find(" PIBIC-EM") != -1):
        posicao_final_trabalho = nome.find("- PIBIC-EM") - 21
    elif(nome.find("- Bolsista") != -1):
        posicao_final_trabalho = nome.find("- Bolsista")
    elif(nome.find("Curso:") != -1):
        posicao_final_trabalho = nome.find("Curso:") - 21

    else:
        return None

    # Cria-se agora uma nova string que possui tanto o nome do trabalho como o nome do autor
    nome = nome[:posicao_final_trabalho]


    # Retorna-se o valor dessa string
    return nome





# Função responsável por retirar o email do nome
# No Enic 17 foi necessário essa mudança, pois o algoritmo atual armazenava o email junto a string do nome
def retira_email(nome_e_email):

    frase: str= nome_e_email

    palavras: list = frase.split()

    palavra_final: str = ""

    for palavra in palavras:
        palavra_final += (palavra if '@' not in palavra else '') + ' '

    

    return palavra_final

 

   



def retira_nome_trabalho(nome_autores: list,nome_autor_trabalho: str, nome_autor:list):

    for nome in nome_autores:
        if(nome_autor_trabalho.find(nome) != -1):
            nome_autor.append(nome)
            texto_autor = nome_autor_trabalho.replace(nome, "")
            
            return texto_autor



# Função responsável por escrever o texto inteiro em um arquivo 
def escreve_texto(indice:int , nome_projeto: str, nome_autor):
    
    # Criação de um dicionário
    resumo:dict = {}
    # Armazena-se nas chaves indice, titulo e texto todo o conteudo do resumo e retora-se esse dicionario
    resumo["indice"] = indice
    resumo["titulo"] = nome_projeto
    resumo["autor"] = nome_autor[0]
    #Printa-se tudo que está após resumo, utilizamos posicaoResumoInicial + 8, pois 8 é o tamanho da string resumo e queremos iniciar após ela
    #Logo, termina quando achar a string "Palavras-Chave: que está no índice posicaoResumoFinal"
    resumo["texto"] = pageConteudo[posicaoResumoInicial + 8:posicaoResumoFinal]

    
    return resumo



def abre_orientadores(orientadores_arquivo):
    arq = open(orientadores_arquivo, 'r')

    linhas = arq.readlines();
    orientadores = list()

    for linha in linhas:
        orientadores.append(linha)
    
    return orientadores



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
        nome_autores:list = nome_alunos(arquivo_alunos)
        
        orientadores = abre_orientadores(nome_orientadores)


    
        # Chamada da função para retirada do nome do trabalho junto ao nome do autor
        nomeTemporario: str = retira_trabalho_autor()
        
    

       

        
        # A partir da edicao 18 do enic, as páginas do resumo foram dividas entao não foi achado o nome do autor, logo a função deve retornar nulo e devemos pular de página
        if(nomeTemporario == None):
        
            quantidadeResumos +=1
            no_read += 1
            print(pageConteudo)
            break
            continue
        

       
        
       
        nome_autor: list = [] # Nome do autor para ser adicionado nos dados    
        # Com o nome temporario do trabalho junto ao nome do autor, podemos agora retirar o nome do autor do trabalho e deixar somente o nome do projeto
        # em algumas enic, ficará junto também o email do aluno
        nomeTrabalho: str = retira_nome_trabalho(nome_autores , nomeTemporario, nome_autor)

        if(nomeTrabalho == None) :
            no_read += 1
            print(nomeTemporario)
            continue
        
        
    
        


        # Vamos retirar o email do usuario, caso ele exista
        #if(nomeTrabalho.find("@") != -1):
        
         #   nomeTrabalho = retira_email(nomeTrabalho)
        
        
    
        
        posicaoResumoInicial: int = 0
        #Vamos pegar a posição do início do resumo daquela página
        if pageConteudo.find("Resumo:") != - 1:
            posicaoResumoInicial = pageConteudo.find("Resumo:")
        else:
            posicaoResumoInicial = pageConteudo.find("RESUMO") - 1

        #Posicao Final do resumo é quando achamos a string "Palavras-Chave:"
        posicaoResumoFinal  = pageConteudo.find("Palavras-Chave:")

        

        
        
        #Recebe-se o dicionário
        resumo_dict: dict= escreve_texto(indiceResumo, nomeTrabalho, nome_autor)
        #Adiciona-se o dicionario na lista de resumos
        resumos.append(resumo_dict.copy())
        quantidadeResumos += 1      # Aumenta-se em um a variável de controle do loop
        indiceResumo += 1           # Aumenta-se em um o índice do resumo
        nomeTrabalho = ''                   # Limpa-se o nome do trabalho

    with open(resumo_nome, 'w') as resumo_js:
        json.dump(resumos, resumo_js, indent = 4, ensure_ascii=False)
    resumo_js.close()
   
    print(no_read)
    resumo_pdf.close()
    
    

    


















