#Código responsável por criar um json dos orientadores data o json de projetos daquele ano
import json

def abre_projetos(path):
    '''Retorna a lista de dicionario de projetos'''
    with open(path) as projeto:
        data = json.load(projeto)
        
    return data


def trabalhos_orientados_orientadores(data_projetos, data_orientadores):
    
    for orientador in data_orientadores:
        orientador_nome = orientador["Nome"]
        trabalhos_orientados = list()
        
        for projeto in data_projetos:
            if orientador_nome == projeto["Orientador:"]:
                trabalhos_orientados.append(projeto["id"])
        
        orientador["Projetos"] = trabalhos_orientados
        

def read_orientadores(data_projetos):
    """Codigo responsável por retirar todos os orientadores unicos"""
    
    orientadores_visited = list()
    orientadores_data = list()
    i = 0
    for projeto in data_projetos:
        orientador_dic = dict()
        
        if projeto["Orientador:"] not in orientadores_visited:
            orientadores_visited.append(projeto["Orientador:"])
            orientador_dic["id"] = i
            orientador_dic["Nome"] = projeto["Orientador:"]
            orientador_dic["Area"] = projeto["Area:"]
            orientador_dic["SubArea"] = projeto["SubArea:"]
            i += 1
            orientadores_data.append(orientador_dic)
    
    
    return orientadores_data

def main():
    path_projetos = 'projetos2017.json'
    orientadores_path = 'orientadores17.json'
    
    data_projetos = abre_projetos(path_projetos)
    orientadores_data = read_orientadores(data_projetos)
    trabalhos_orientados_orientadores(data_projetos, orientadores_data)
    
    with open (orientadores_path, 'w') as orientadores_json:
        json.dump(orientadores_data, orientadores_json, indent=4, ensure_ascii=False)






























if __name__ == '__main__':
    main()
