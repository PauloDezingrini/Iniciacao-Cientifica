# -*- coding: utf-8 -*-
from TSPfile import TSPfile
from solution import *
from pathlib import Path


while True:

    arquivo_a_ser_lido = input("Digite o nome do arquivo que será lido: ")

    files_folder = Path(
        'C:/Users/Paulo Dezingrini/Documents/Codes/Python/Iniciacao-Cientifica/Instâncias/')
    file = files_folder / arquivo_a_ser_lido

    file = TSPfile(file)

    lista_de_pontos = file.getList()
    matrizDistancias = file.getMatriz()

    numero_de_pontos = int(
        input("Digite o numero de pontos que terá a solução: "))

    solucao = Solution(numero_de_pontos, lista_de_pontos,
                       matrizDistancias, file.getDimension())

    # solucao.findSolutionSemiRandomHVMP(4)
    # solucao.findSolutionHVMP()
    # solucao.findSolutionRandomHVMP2(2)
    # solucao.graspRVND(100, 2)
    solucao.findSolutionRandomHVMP(numero_de_pontos,1)
    # solucao.buscaLocalRVND()

    # solucao.plotarSolucao(arquivo_a_ser_lido)

    solucao.ILS(100)
    solucao.printDist()
    solucao.plotarSolucao(arquivo_a_ser_lido)
