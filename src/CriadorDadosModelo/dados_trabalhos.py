""" Codigo responsável por criar os dados dos trabalhos
 Como nome do projeto, título do projeto, orientador area e sub area
 Precisa do aval total com todos os trabalhos para ser feito
 Foi notado que chico alocou apenas os trabalhos pelo nome do projeto deles
 por isso que a quantia de trabalos dele está reduzida
 Pois existem vários trabalhos com o mesmo titulo do plano
 Cada projeto terá seu id que é o id da lista"""
import json
import unicodedata
import pandas as pd


# Abre o arquivo de aval e associa cada orientador ao seu projeto
def abre_arquivo_aval(caminho: str):
    """ Função responsável por abrir o arquivo de aval """
    file = pd.read_csv(caminho, sep=',', encoding='UTF-8')

    # Cria array de cada coluna e então verifica se ja foi incluso pelo nome
    # do projeto
    nome_projetos_totais = file['Projeto:'].tolist()
    nome_plano_totais = file['Plano:'].tolist()
    nome_orientador_totais = file['Orientador:'].tolist()
    areas_totais = file['Área:'].tolist()
    subareas_totais = file['Subárea:'].tolist()

    tamanho_csv = len(nome_projetos_totais)
    dados_projetos = list()

    counter = 0

    # Lê-se cada linha do projeto analisando pelo nome do projeto se ja foi
    # incluido caso não foi incluido pegamos todos os dados
    # e guardamos em um json
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

        if inserido is False:
            dados_projetos.append(dados)
            counter += 1

    return dados_projetos


def abre_alocacao(caminho):
    """Função responsável por abrir as alocações de chico e retornar-los"""
    file = pd.read_csv(caminho, sep=',', encoding='UTF-8')
    return file["Projeto:"].tolist()


def main():
    """Função main"""
    caminho_aval = "../AlocacoesEAval/relatorios2016.csv"
    caminho_alocacao = "../AlocacoesEAval/2016.csv"
    trabalhos_nome = "projetos2016.json"
    caminho_nao_encontrado = "nao_encontrados.txt"

    projetos_lidos = abre_arquivo_aval(caminho_aval)
    projetos_alocados = abre_alocacao(caminho_alocacao)

    alocados = list()
    lidos = list()
    # Vamos agora verificar se lemos de fato todos os projetos
    # Primeiro tratamos todas as strings e armazenamos em duas listas
    for alocado in projetos_alocados:
        alocado_processada = unicodedata.normalize("NFD", alocado)
        alocado_processada = alocado_processada.encode("ascii", "ignore")
        alocado_processada = alocado_processada.decode("utf-8")
        alocado_processada = alocado_processada.lower().lstrip().rstrip()
        alocados.append(alocado_processada)

    for projetos in projetos_lidos:
        projeto_processado = unicodedata.normalize("NFD", projetos["Projeto:"])
        projeto_processado = projeto_processado.encode("ascii", "ignore")
        projeto_processado = projeto_processado.decode("utf-8")
        projeto_processado = projeto_processado.lower().lstrip().rstrip()
        lidos.append(projeto_processado)
    counter = 0
    nao_encontrados = list()
    # Verifica se todos os trabalhos estão e salva os que não foram lidos
    for lido in lidos:
        encontrado = False
        for alocado in alocados:
            if lido == alocado:
                counter += 1
                encontrado = True
        if encontrado is False:
            nao_encontrados.append(lido)

    print(f'Foram encontrados {counter} projetos\n')

    with open(caminho_nao_encontrado, "w") as file:
        for text in nao_encontrados:
            file.write(text + '\n')
    file.close()

    with open(trabalhos_nome, 'w') as trabalhos_js:
        json.dump(projetos_lidos, trabalhos_js, indent=4, ensure_ascii=False)
    trabalhos_js.close()
    return 0


if __name__ == '__main__':
    main()
