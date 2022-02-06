# -*- coding: utf-8 -*-
import imp
from TSPfile import TSPfile
from solution import *
from pathlib import Path


while True:

    arquivo_a_ser_lido = input("Digite o nome do arquivo que será lido: ")

    files_folder = Path('C:/Users/Paulo Dezingrini/Desktop/Iniciacao-Cientifca/Instâncias/')
    file = files_folder / arquivo_a_ser_lido

    file = TSPfile(file)

    lista_de_pontos = file.getList()
    matrizDistancias = file.getMatriz()

    numero_de_pontos = int(input("Digite o numero de pontos que terá a solução: "))

    solucao = Solution(numero_de_pontos,lista_de_pontos,matrizDistancias,file.getDimension())

    solucao.findSolutionHVMP()
    solucao.busca_local_addDrop()
    solucao.printPath()
    solucao.printDist()
