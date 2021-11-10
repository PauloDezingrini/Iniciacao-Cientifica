# -*- coding: utf-8 -*-
from TSPfile import TSPfile
from solucao import *


while True:

    arquivo_a_ser_lido = input("Digite o nome do arquivo que será lido: ")

    file = TSPfile(arquivo_a_ser_lido)

    lista_de_pontos = file.getList()
    matrizDistancias = file.getMatriz()

    numero_de_pontos = int(input("Digite o numero de pontos que terá a solução: "))

    solucao = Solucao(numero_de_pontos,lista_de_pontos,matrizDistancias,file.getDimension())

    MetodoResolucao = int(input("Digite o método que será usado para achar a solução\n 1-Randomico, 2-Vizinho mais proximo, 3-Inserção mais barata,4-VMPA ,5-Modelo : "))
    if MetodoResolucao == 1:
        solucao.encontrarSolucaoRandomica()
    elif MetodoResolucao == 2:
        solucao.encontrarSolucaoVizinhoProximo()
    elif MetodoResolucao == 3:
        solucao.encontrarSolucaoInsercaoMaisBarata()
    elif MetodoResolucao == 4:
        # dimension = file.getDimension()
        # if dimension >= 200:
        #     solucao.encontrarSolucaoVMPA(0.01)
        # elif dimension >= 30:
        #     solucao.encontrarSolucaoVMPA(0.05)
        # elif dimension >= 15:
        #     solucao.encontrarSolucaoVMPA(0.1)
        # else:
        #     solucao.encontrarSolucaoVMPA(0.15)
        solucao.encontrarSolucaoVMPA(0.2)
    elif MetodoResolucao == 5:
        solucao.encontrarSolucaoModelo()
    
    # print(solucao)
    solucao.getPontos()
    solucao.plotarSolucao(arquivo_a_ser_lido)

    continuar = input("Deseja realizar outra leitura? (S p/ sim) (N p/ não)" )

    if continuar == 'N':
        break