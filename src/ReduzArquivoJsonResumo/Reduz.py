# Código responsável por reduzir o tamanho total do arquivo de resumos json
# Necessário o resultado da alocação do ano correspondente
# Aval completo do relatório
# Arquivo json de resumos
import json
import pandas as pd

# Abre o arquivo de resumos
def abre_arquivo_resumos(caminho: str):
    
    trabalhos = list() 
    with open(caminho) as file:
        trabalhos = json.load(file)
    file.close()
    
    return trabalhos

# Abre o arquivo de alocao e retorna apenas o nome dos projetos
def abre_arquivo_alocacao(caminho: str):
    file = pd.read_csv(caminho, sep=',', encoding='UTF-8')
    nome_projetos = file['Projeto:'].unique().tolist()

    return nome_projetos

def abre_arquivo_aval(caminho: str):

    file = pd.read_csv(caminho, sep=',', enconding='UTF-8')
    

def main():
    caminho_resumo = "../resumoOrientadores/resumoOrientadores14.json"
    caminho_alocacao = "../AlocacoesEAval/2014.csv"
    caminho_aval = "../AlocacoesEAval/relatorios2014.csv"

    trabalhos = abre_arquivo_resumos(caminho_resumo)
    trabalhos_alocados = abre_arquivo_alocacao(caminho_alocacao)
    return 0

if __name__ == '__main__':
    main()  