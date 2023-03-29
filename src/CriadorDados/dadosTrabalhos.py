# Codigo responsável por criar os dados dos trabalhos
# Como nome do projeto, título do projeto, orientador area e sub area
# Precisa do aval total com todos os trabalhos para ser feito
# Foi notado que chico alocou apenas os trabalhos pelo nome do projeto deles, por isso que a quantia de trabalos dele está reduzida
# Pois existem vários trabalhos com o titulo de projeto diferente do plano
# Cada projeto terá seu id que é o id da lista
import pandas as pd
import json

# Abre o arquivo de aval e associa cada orientador ao seu projeto
def abre_arquivo_aval(caminho: str):

    file = pd.read_csv(caminho, sep=',', encoding='UTF-8')
    
    # Cria array de cada coluna e então verifica se ja foi incluso pelo nome do projeto
    nome_projetos_totais = file['Projeto:'].tolist()
    nome_plano_totais = file['Plano:'].tolist()
    nome_orientador_totais = file['Orientador:'].tolist()
    areas_totais = file['Área:'].tolist()
    subareas_totais = file['Subárea:'].tolist()

    tamanho_csv = len(nome_projetos_totais)
    dados_projetos = list()

    # Primeiro vamos criar uma lista de orientadores, contendo sua área e subárea

    orientadores = list() # Lista de orientadores

    # Como estamos lendo o csv, verificamos se naquela linha do csv, meu orientador já foi adicionado a lista de orientadores
    # Caso não, adicionamos os dados corretos referente aquela linha do orientador
    for i in range(tamanho_csv):
        dados = dict()
        alocado = False # Verifica se o orientador já está na lista
        for orientador in orientadores:
            if nome_orientador_totais[i] == orientador['Orientador:']:
                alocado = True

        # Se o orientador não foi alocado
        if alocado == False:
            dados['Orientador:'] = nome_orientador_totais[i]
            dados['Area:'] = areas_totais[i]
            dados['SubArea:'] = subareas_totais[i]
            orientadores.append(dados)

    

    counter = 0
    # Lê-se cada linha do projeto analisando pelo nome do projeto se já foi incluido ou não, caso não foi incluido pegamos todos os dados e guardamos em um json
    for i in range(tamanho_csv):
        dados = dict()
        dados['id'] = counter
        dados['Projeto:'] = nome_projetos_totais[i]
        dados['Plano:'] = nome_plano_totais[i]
        dados['Orientador:'] = nome_orientador_totais[i]
        dados['Area:'] = areas_totais[i]
        dados['SubArea:'] = subareas_totais[i]
        inserido = False

        for dados_inserido in dados_projetos:
            if dados_inserido['Projeto:'] == dados['Projeto:']:
                inserido = True
        
        if inserido == False:
            dados_projetos.append(dados)
            counter += 1

    return dados_projetos



def main():

    caminho_aval = "../AlocacoesEAval/relatorios2014.csv"
    caminho_alocacao = "../AlocacoesEAval/2014.csv"
    trabalhos_nome = "projetos2014.json"

    trabalhos_totais = abre_arquivo_aval(caminho_aval)
    


    #Comparação se de fato todos os trabalhos foram pegos
    with open(trabalhos_nome, 'w') as trabalhos_js:
        json.dump(trabalhos_totais, trabalhos_js, indent = 4, ensure_ascii=False)
    trabalhos_js.close()
    return 0











if __name__ == '__main__':
    main()