from ponto import *
import random

import matplotlib.pyplot as plt

class Solucao(object):
    def __init__(self,numero_de_pontos):
        self.__pontos = []
        self.__distTotal = 0
        self.__numero_de_pontos = int(numero_de_pontos)

    def __str__(self):
        for ponto in self.__pontos:
            print("Ponto de numero:",ponto.getNumero()," com coordenadas: ",ponto.getX()," , ",ponto.getY())
        return "Com uma distancia total de " + str(self.__distTotal)

    def calcularDistTotal(self,matriz_de_distancia):
        distTotal = 0
        for i in range(self.__numero_de_pontos - 1):
            n1 = self.__pontos[i].getNumero()
            n2 = self.__pontos[i + 1].getNumero()
            # O - 1 é devido ao fato da lista começar em 0 , não em 1 , portanto o ponto 1 está na posição 0 , o ponto 2 na posição e por ai vai 
            distTotal += matriz_de_distancia[n1 - 1][n2 - 1]
        self.__distTotal = distTotal


    def encontrarSolucaoRandomica(self,lista_de_pontos):
        # A lista aux é necessária para poder remover os pontos já utilizados na solução da lista sem alterar a lista de pontos.
        # Já que o processo para encontrar uma solução poderá ocorrer mais de 1 vez
        aux = lista_de_pontos
        # Como a leitura é feita de forma a seguir o numero dos pontos e o primeiro ponto de toda solução tem que ser o ponto 1
        # Podemos fazer essa atribuição diretamente com a posicao 0 da lista de pontos
        self.__pontos.append(aux[0])
        aux.pop(0)
        # Enquanto o tamanho da solução(__pontos) for menor que o numero de pontos pedidos ele escolhe uma posicao aleatoaria do array
        # Entao adiciona essa solucao ao vetor __pontos e deleta do vetor auxiliar para evitar repeticoes
        while(len(self.__pontos)<self.__numero_de_pontos):
            index = random.randint(0,len(aux)-1)
            self.__pontos.append(aux[index])
            aux.pop(index)

    def plotarSolucao(self,nome_do_arquivo):
        x = []
        y = []
        for ponto in self.__pontos:
            x.append(ponto.getX())
            y.append(ponto.getY())
        plt.plot(x,y)
        plt.xlabel('Coordenadas x')
        plt.ylabel('Coordenadas y')
        titulo = 'Solução aleatória para ' + nome_do_arquivo 
        subtitle = 'Distância Total k = ' + str(self.__distTotal)
        plt.title(subtitle)
        plt.suptitle(titulo)
        for ponto in self.__pontos:
            plt.text(ponto.getX(),ponto.getY(),str(ponto.getNumero()))
        plt.show()
        return plt
        