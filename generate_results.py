# -*- coding: utf-8 -*-
from TSPfile import TSPfile
from solution import *
from pathlib import Path
from openpyxl import Workbook


file_to_read = 0
while file_to_read <= 0 or file_to_read > 4:
    file_to_read = int(input(
        "1 = n/4 \n2 = n/2 \n3 = 3n/4 \n4 = Selecionadas \nEscolha o valor de K: "))

if file_to_read == 1:
    file_to_read = "InstanciasArtigo-n4.txt"
elif file_to_read == 2:
    file_to_read = "InstanciasArtigo-n2.txt"
elif file_to_read == 3:
    file_to_read = "InstanciasArtigo-3n4.txt"
elif file_to_read == 4:
    file_to_read = "Instâncias selecionadas.txt"


files_folder = Path(
    'C:/Users/Paulo Dezingrini/Desktop/Iniciacao-Cientifca/Arquivos de teste/')
test_file = files_folder / file_to_read

test_file = open(test_file, 'r')
sheet_file = Workbook()

sheet1 = sheet_file.active
first_line = ("Instâncias", "Número de pontos", "Distância")

sheet1.append(first_line)

for line in test_file:

    line = line.strip('\n')
    line = line.split('-')

    file_name = line[0] + '.tsp'

    print(f'Iniciando a execução do {line[0]}')

    files_folder = Path(
        'C:/Users/Paulo Dezingrini/Desktop/Iniciacao-Cientifca/Instâncias/')
    file = files_folder / file_name

    file = TSPfile(file)

    point_list = file.getList()
    dist_matrix = file.getMatriz()
    points_number = line[1]

    solution = Solution(points_number, point_list,
                        dist_matrix, file.getDimension())

    # Alterar ou inserir aqui os métodos que serão utilizados para gerar os testes

    solution.findSolutionHIMB()
    # solution.buscaLocalRVND()
    solution.ILS(100)

    # solution.findSolutionHIMB()
    # solution.busca_local_addDrop()
    # solution.busca_local_troca()

    print(f'Terminando a execução do {line[0]}')
    print("----------------------------------------------")

    new_line = (line[0], int(points_number), solution.getDist())
    sheet1.append(new_line)

test_file.close()
sheet_file.save("resultados.xlsx")
