"""Código responsável por alinhar na mesma sequencia o arquivo de resumo 
 de orientadores com o criado com projetos"""
import json


# Abre arquivo de resumo dos orientadores
def abre_orientadores(path_orientadores):
    """Retorna os dados do resumo dos orientadores"""
    with open(path_orientadores) as file:
        data = json.load(file)

    return data


def abre_projetos(path_projetos):
    """Retorna o dicionario dos projetos"""
    with open(path_projetos) as file:
        data = json.load(file)

    return data


def main():
    path_orientadores = "resumoOrientadores16.json"
    path_projetos = "../CriadorDadosModelo/projetos2016.json"
    resumo_nome = "resumoOrientadores16Alin.json"
    orientadores_resumo = abre_orientadores(path_orientadores)
    projetos = abre_projetos(path_projetos)

    orientadores_resumo_alin = list()

    # Vamos percorrer cada linha dos projetos e dps percorrer cada linha
    # de resumos dos meus orientadores
    # Quando for achado o mesmo projeto no resumo, adicionamos
    # uma nova linha de resumo id e adicionamos na lista
    for projeto in projetos:
        for resumo in orientadores_resumo:
            if resumo['Projeto:'] == projeto['Projeto:']:
                orientadores_resumo_alin.append(resumo)

    
    # Responsável por criar o json do resumo dos orientadores
    with open(resumo_nome, 'w') as resumo_js:
        json.dump(orientadores_resumo_alin, resumo_js, indent=4, ensure_ascii=False)
    resumo_js.close()


if __name__ == '__main__':
    main()
