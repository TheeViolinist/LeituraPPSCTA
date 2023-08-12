import json
import pandas as pd


def open_alocacao(path):
    main_df = pd.read_csv(path, sep=',', encoding='UTF-8')
    avaliadores = main_df['Avaliador 1:'].unique().tolist() + main_df['Avaliador 2:'].unique().tolist()
    print(f'Tamanho de avaliadores antes: {len(avaliadores)}')
    avaliadores = list(set(avaliadores))
    print(f'Tamanho de avaliadores depois: {len(avaliadores)}')
    

def main():
    alocacoes_path = "2014.csv"
    alocacao_data = open_alocacao(alocacoes_path)
    








if __name__ == '__main__':
    main()