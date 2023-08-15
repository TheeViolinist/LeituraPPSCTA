import json
import sys
import pandas as pd
import unicodedata



class Instance:
    def __init__(self, allocation_file, data_file, year):
        """Abre arquivo de alocações e pega todos os projetos alocados"""
        self.allocation_df = pd.read_csv(allocation_file, sep=',', encoding="UTF-8")
        """Abre arquivo de aval contendo todos os dados sobre os projetos"""
        self.data_df = pd.read_csv(data_file, sep=',', encoding="UTF-8")
        self.year = int(year)


    def write_json(self, data):
        path_projects = f'DadosTrabalhos/projetos{self.year}.json'
        with open(path_projects, 'w') as file_js:
            json.dump(data, file_js, indent=4, ensure_ascii=False)
        file_js.close()


    """Função responsável por criar o arquivo de projetos referente ao aval e alocação"""
    """Os trabalhos foram alocados pelo nome do projeto dele, os trabalhos possuem nome de projeto iguais"""
    """Sendo assim, pegamos o primeiro trabalho com aquele nome de projeto e criamos um arquivo contendo
    Seus dados como orientador, área e subárea daquele projeto"""
    def write_projects(self):
            
        name_projects = self.data_df["Projeto:"].tolist()
        name_plans = self.data_df["Plano:"].tolist()
        name_advisors = self.data_df["Orientador:"].tolist()
        areas = self.data_df["Área:"].tolist()
        subarea = self.data_df["Subárea:"].tolist()

        len_csv = len(name_projects)
        data_projects_total = list()

        counter = 0

        for i in range(len_csv):
            data = dict()
            data["id"] = counter
            data["Projeto:"] = name_projects[i]
            data["Plano:"] = name_plans[i]
            data["Orientador:"] = name_advisors[i]
            data["Area:"] = areas[i]
            data["SubArea:"] = subarea[i]

            insert = False
            for project_insert in data_projects_total:
                if project_insert["Projeto:"] == data["Projeto:"]:
                    insert = True
            
            if insert is False:
                data_projects_total.append(data)
                counter += 1

        """Verificando se todos foram lidos de fato"""
        projects_allocate = self.allocation_df["Projeto:"].to_list()
        print(f'Fora encontrados {len(data_projects_total)} de {len(projects_allocate)}')

        self.write_json(data_projects_total)

def main():

    if len(sys.argv) < 4:
        sys.exit("Digite pelo menos 4 argumentos da forma: python3 alocacao.csv relatorio.csv ano")
    
    allocation_file = sys.argv[1] # Arquivo de alocação feita por Chico
    data_file = sys.argv[2] # Arquivo de dados, contendo informações sobre os trabalhos daquele ano
    year = sys.argv[3] # Ano que está sendo analisado
    instance_data = Instance(allocation_file, data_file, year)
    instance_data.write_projects()
    print("Oi")












if __name__ == '__main__':
    main()