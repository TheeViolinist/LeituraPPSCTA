import json
import sys
import pandas as pd
import unicodedata
import PyPDF2



class Project:
    def __init__(self, allocation_file, data_file, year):
        """Abre arquivo de alocações e pega todos os projetos alocados"""
        self.allocation_df = pd.read_csv(allocation_file, sep=',', encoding="UTF-8")
        """Abre arquivo de aval contendo todos os dados sobre os projetos"""
        self.data_df = pd.read_csv(data_file, sep=',', encoding="UTF-8")
        self.year = int(year)
        self.projects_total = None # Lista contendo todos os projetos
        self.advisors = None #Lista contendo todos os orientadores


    def get_projects(self):
        return self.projects_total
    
    def get_advisors(self):
        return self.advisors

    def get_year(self):
        return self.year
    

    def write_json(self, data, is_project):
        if is_project:
            path = f'DadosTrabalhos/projetos{self.year}.json'
        else:
            path = f'DadosTrabalhos/orientadores{self.year}.json'

        with open(path, 'w') as file_js:
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

        # Salva todos os projetos
        self.projects_total = data_projects_total
        self.write_json(data_projects_total, True)

    """Função responsável por criar um arquivo json contendo os orientadores daquele projeto"""
    def write_advisors(self):
        advisors_visited = list()
        advisors_data = list()
        i = 0

        for project in self.projects_total:
            advisors_dic = dict()

            if project["Orientador:"] not in advisors_visited:
                advisors_visited.append(project["Orientador:"])
                advisors_dic["id"] = i
                advisors_dic["Nome"] = project["Orientador:"]
                advisors_dic["Area"] = project["Area:"]
                advisors_dic["SubArea"] = project["SubArea:"]
                i += 1
                advisors_data.append(advisors_dic)


        
        for advisor in advisors_data:
            advisor_name = advisor["Nome"]
            papers_advisor = list()

            for project in self.projects_total:
                if advisor_name == project["Orientador:"]:
                    papers_advisor.append(project["id"])

            advisor["Projetos"] = papers_advisor
        
        self.advisors = advisors_data
        self.write_json(advisors_data, False)

                
def main():

    if len(sys.argv) < 4:
        sys.exit("Digite pelo menos 4 argumentos da forma: python3 alocacao.csv relatorio.csv ano")
    
    allocation_file = sys.argv[1] # Arquivo de alocação feita por Chico
    data_file = sys.argv[2] # Arquivo de dados, contendo informações sobre os trabalhos daquele ano
    year = sys.argv[3] # Ano que está sendo analisado
    project_data = Project(allocation_file, data_file, year)
    # Escrita do arquivo de projeto
    project_data.write_projects()
    project_data.write_advisors()
    












if __name__ == '__main__':
    main()