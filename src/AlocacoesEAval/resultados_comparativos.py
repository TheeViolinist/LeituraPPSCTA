# Código responsável por analisar os resultados da planilha
# de alocações tendo em mente o arquivo json total, para analisar os resultados de chico
import json
import panda as pd


projetos_path = "../CriadorDados/projetos2014.json"
alocacoes_path = "2014.csv"

def abre_projetos(projetos_path):

    with open(projetos_path) as file:
        data = json.load(file)
    
    return data

def abre_arquvivo_alocacao

def main():
    projetos = abre_projetos(projetos_path)
    











if __name__ == "__main__":
    main()