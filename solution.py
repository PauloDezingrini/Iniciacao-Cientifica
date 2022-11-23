from copy import copy
from math import ceil, floor
from operator import ne
from random import randint
from turtle import pos
from mip import *

import matplotlib.pyplot as plt
import heapq

from numpy import less

from ponto import *


class Solution(object):
    """ Funções básicas da classe """
    def __init__(self, n_pontos, lista_de_pontos, matriz_dist, dimension): 
        self.__solucao = []
        self.__dist = 0
        self.__n_pontos = int(n_pontos)
        self.__lista_de_pontos = lista_de_pontos
        self.__matriz_dist = matriz_dist
        self.__solType = ""
        self.__dimension = dimension

    def getDist(self):
        return round(self.__dist, 2)

    def getNPoints(self):
        return self.__n_pontos

    def getSolLen(self):
        return len(self.__solucao)

    def getSolution(self):
        return self.__solucao

    def setSolution(self, solution):
        self.__solucao = solution

    def printDist(self):
        print(round(self.__dist, 2))

    def printSolution(self):
        for i in range(len(self.__solucao) - 1):
            n1 = self.__solucao[i] - 1
            n2 = self.__solucao[i + 1] - 1
            print(self.__matriz_dist[n1][n2], end="->")

    def printPath(self):
        for i in self.__solucao:
            print(i, end="->")
        print('\n')

    def calculateDist(self, solution):
        dist = 0
        for i in range(len(solution) - 1):
            n1 = solution[i]
            n2 = solution[i + 1]
            dist += self.__matriz_dist[n1 - 1][n2 - 1]
        return round(dist, 2)

    """ Funções auxiliares """

    # Dado um ponto(index) retorna o ponto mais próximo deste que não esteja na solução
    def closerPoint(self, index):
        saiDe = self.__solucao[index] - 1
        lesserDist = -1
        for i in range(self.__dimension):
            dist = self.__matriz_dist[saiDe][i]
            if((dist <= lesserDist) or (lesserDist == -1)):
                if (i+1) not in self.__solucao:
                    lesserDist = dist
                    newPoint = i
        return newPoint, lesserDist

    def closeToTheWay(self, n):
        pq = []
        for i in self.__solucao:
            for j in range(self.__dimension):
                if i - 1 != j and j+1 not in self.__solucao:
                    heapq.heappush(
                        pq, (self.__matriz_dist[i - 1][j], (i, j+1)))
        pq = heapq.nsmallest(n, pq)
        return pq

    def closeToThePoint(self, i):
        lesserDist = -1
        for j in range(self.__dimension):
            dist = self.__matriz_dist[i][j]
            if (dist < lesserDist or lesserDist == -1) and (j + 1 not in self.__solucao):
                lesserDist = dist
                point = j + 1
        return point

    def longerDist(self, n):
        pq = []
        for i in range(1, self.__n_pontos - 1):
            I = self.__solucao[i] - 1
            nextI = self.__solucao[i + 1] - 1
            heapq.heappush(pq, (self.__matriz_dist[I][nextI], nextI + 1))
        pq = heapq.nlargest(n, pq)
        return pq

    def getNewRandomPoint(self):
        i = 1
        while i in self.__solucao:
            i = randint(1, self.__dimension)
        return i

    # Dado um ponto retorna a melhor posição que este pode ser inserido na solução
    def getBestPosition(self, point, solution):
        lesserDist = -1
        for i in range(1, len(solution)):
            dist = self.__matriz_dist[point - 1][solution[i] - 1]
            if dist < lesserDist or lesserDist == -1:
                lesserDist = dist
                posToInsert = i
        return posToInsert

    def getCloserNeightboors(self, point):
        d1 = []
        for i in range(self.__dimension):
            if i+1 != point and i+1 not in self.__solucao:
                d1.append((self.__matriz_dist[point - 1][i], i + 1))
        d1.sort()
        return d1

    """ Solução modelo"""
    def encontrarSolucaoModelo(self):
        self.__solType = "Modelo"
        # size1 é utilizado em restrições que iniciam desde o primeiro ponto , enquanto o size2 exclui esse ponto
        size1 = set(range(len(self.__matriz_dist[0]) -1))
        size2 = set(range(1,len(self.__matriz_dist[0])-1))

        model = Model()
        x = [[model.add_var(var_type=BINARY) for j in size1] for i in size1]
        y = [model.add_var(var_type=BINARY) for i in size1]
        F = [[model.add_var() for i in size1] for j in size1]

        model.objective = minimize(xsum(self.__matriz_dist[i][j]*x[i][j] for i in size1 for j in size1))

        # Restricao 2 : Garante que só haverá uma rota saindo do ponto inicial
        model += xsum(x[0][j] for j in size2) == 1
        # Restricao 3 : Garante que não terá nenhuma rota chegando no ponto inicial
        model += xsum(x[i][0] for i in size2) == 0

        # Restricoes 4 e 5 : Garantem que só haverá uma rota saindo e uma chegando em cada ponto
        for j in size1:
            model += xsum(x[i][j] for i in size1 if i!=j) <= 1

        for i in size1:
            model += xsum(x[i][j] for j in size1 if i!=j) <= 1
        
        # Restriçao 6 : Garante que o número de pontos do modelo será igual ao número de pontos requisitado.
        model += xsum(y[i] for i in size1) == self.__n_pontos

        # Restriçao 7
        for i in size2:
            model += (xsum(F[h][i]for h in size1) - xsum(F[i][j] for j in size1)) == y[i]
        # Restriçao 8
        for i in size1:
            for j in size1:
                model+= F[i][j] <= (self.__n_pontos - 1)*x[i][j]
        # Restriçao 9 : 
        for j in size1:
            model += (xsum(x[i][j] for i in size1) - xsum(x[j][h] for h in size2)) <=1

        model.optimize(max_seconds=3600)
        pontos_utilizados = []
        if model.num_solutions:
            self.__dist = model.objective_value
            posSaida = 0
            pontos_utilizados.append(0)
            while True:
                for i in size2:
                    if(x[posSaida][i].x >= 0.90 and i not in pontos_utilizados):
                        pontos_utilizados.append(i)
                        posSaida = i
                        break
                if(len(pontos_utilizados) == self.__n_pontos):
                    break
            for i in range(self.__n_pontos):
                self.__solucao.append(pontos_utilizados[i] + 1)


    """ Heuristícas construtivas """

    """
    Versão do vizinho mais próximo guloso.
    def findSolutionHVMP(self):  # Heuristíca do vizinho mais próximo
        if self.__solucao == []:
            self.__solucao.append(1)
        cont = len(self.__solucao)
        while(cont < self.__n_pontos):
            pos, dist = self.closerPoint(-1)
            self.__solucao.append(pos + 1)
            self.__dist += dist
            cont += 1
        self.__solType = "HVMP"
    """

    """
    Versão do vizinho mais próximo aleatório utilizando porcentagens(Alfa)
    def findSolutionRandomHVMP(self, n_points, alfa):
        self.__solucao.append(1)
        neightboors = []
        cont = 1
        while(cont < n_points):
            neightboors = self.getCloserNeightboors(self.__solucao[-1])
            m = max(0, floor(alfa*len(neightboors) - 1))
            r = randint(0, m)
            self.__solucao.append(neightboors[r][1])
            cont += 1
        self.__dist = self.calculateDist(self.__solucao)
    """

    def findSolutionRandomHVMP(self, n_points, m):
        if self.__solucao == []:
            self.__solucao.append(1)
        neightboors = []
        cont = 1
        while(cont < n_points):
            if len(self.__solucao) > self.__n_pontos:
                break
            neightboors = self.getCloserNeightboors(self.__solucao[-1])
            m1 = min(len(neightboors), m)
            r = randint(0, m1 - 1)
            self.__solucao.append(neightboors[r][1])    
            self.__dist += neightboors[r][0]
            cont += 1
        self.__dist = round(self.__dist, 2)
        self.__dist = self.calculateDist(self.__solucao)

    def findSolutionRandomHVMP2(self, k):  # Semi-Aleatório 
        self.__solucao.append(1)
        startRandomize = randint(1, floor(0.75*self.__n_pontos))
        endRandomize = startRandomize + floor(self.__n_pontos/4)
        cont = 1
        neightboors = []
        m = 1
        while(cont < self.__n_pontos):
            if cont == startRandomize:
                # print(
                #     f'Inicio da randomização no ponto {self.__solucao[cont - 1]}')
                m = k
            elif cont == endRandomize:
                # print(
                #     f'Fim da randomização no ponto {self.__solucao[cont - 1]}')
                m = 1
            neightboors = self.getCloserNeightboors(self.__solucao[-1])
            m1 = min(len(neightboors), m)
            r = randint(0, m1 - 1)
            self.__solucao.append(neightboors[r][1])
            self.__dist += neightboors[r][0]
            cont += 1
        pass

    """ Buscas locais """

    def busca_local_troca(self):
        better = True
        while better:
            better = False
            s = self.__solucao[:]
            for i in range(1, self.__n_pontos - 1):
                for j in range(i + 1, self.__n_pontos):
                    s[i], s[j] = s[j], s[i]
                    dist = self.calculateDist(s)
                    if dist < self.__dist:
                        self.__dist = dist
                        self.__solucao = s
                        better = True
                    else:
                        s[i], s[j] = s[j], s[i]

    def busca_local_insercao(self):
        better = True
        while better:
            better = False
            for i in range(1, self.__n_pontos):
                for j in range(1, self.__n_pontos):
                    if j != i - 1 and j != i:
                        s = self.__solucao[:]
                        valueToInsert = s[i]
                        s.pop(i)
                        s.insert(j, valueToInsert)
                        dist = self.calculateDist(s)
                        if dist < self.__dist:
                            self.__solucao = s
                            self.__dist = dist
                            better = True

    def busca_local_2OPT(self):
        better = True
        while better:
            better = False
            for i in range(1, self.__n_pontos - 1):
                for j in range(self.__n_pontos - 1, -1, -1):
                    if j > i:
                        s = self.__solucao[:]
                        s[i:j+1] = reversed(s[i:j+1])
                        dist = self.calculateDist(s)
                        if dist < self.__dist:
                            self.__solucao[i:j +
                                           1] = reversed(self.__solucao[i:j+1])
                            self.__dist = dist
                            better = True
                    else:
                        break

    def busca_local_addDrop(self):
        _out = []
        _in = []
        better = True
        pq = self.closeToTheWay(self.__n_pontos)
        while better:
            better = False
            for add in pq:
                if add[1][0] in self.__solucao:
                    index = self.__solucao.index(add[1][0])
                    for i in range(1, self.__n_pontos):
                        if add[1][1] not in self.__solucao and add[1][0] != self.__solucao[i]:
                            s = self.__solucao[:]
                            s.pop(i)
                            s.insert(index+1, add[1][1])
                            dist = self.calculateDist(s)
                            if dist < self.__dist:
                                self.__solucao = s
                                _out.append(self.__solucao[i])
                                _in.append(add[1][1])
                                self.__dist = dist
                                break
        # print("Saiu : ", _out)
        # print("Entrou : ", _in)
        # print("Distancia esperada: ",self.calculateDist(self.__solucao))

    # Para cada ponto na solução, o remove e insere um de fora na melhor posição possível. Fará uso da estratégia de primeira melhora.
    def busca_local_addDrop2(self):
        better = True
        br = False
        while better:
            better = False
            for i in range(1, self.__n_pontos):
                if br:
                    break
                for j in range(1, self.__dimension):
                    if j+1 not in self.__solucao:
                        newSolution = self.__solucao.copy()
                        newSolution.pop(i)
                        posInsert = self.getBestPosition(j+1, newSolution)
                        newSolution.insert(posInsert+1, j+1)
                        newDist = self.calculateDist(newSolution)
                        if newDist < self.__dist:
                            self.__dist = newDist
                            self.__solucao = newSolution
                            br = True
                            better = True
                            break
    """ Metaheurísticas """

    def buscaLocalRVND(self):
        """
            Ao invés de utilizar um vetor com as buscas locais, optei por utilizar simplesmente
            um randint(1,3) que retorna um número aleatório x tal que 1 <= x <= 3
            onde cada número será uma busca local diferente. A relação de buscas locais será:
            1 = Add-Drop
            2 = 2-OPT
            3 = Inserção
        """
        localSearchs = randomizeLocalSearchs()
        k = 1
        while k <= 3:
            oldDist = self.getDist()
            chosenLS = localSearchs.pop()
            if chosenLS == 1:
                self.busca_local_addDrop()
            elif chosenLS == 2:
                self.busca_local_2OPT()
            elif chosenLS == 3:
                self.busca_local_insercao()
            if self.getDist() < oldDist:
                k = 1
                localSearchs = randomizeLocalSearchs()
            else:
                k += 1

    def swapPerturb(self):
        pos1 = -1
        pos2 = -1
        while(pos1 == pos2):
            pos1 = randint(1, len(self.__solucao) - 1)
            pos2 = randint(1, len(self.__solucao) - 1)

        aux = self.__solucao[pos1]
        self.__solucao[pos1] = self.__solucao[pos2]
        self.__solucao[pos2] = aux

    def addDropPerturb(self):
        index = randint(1, len(self.__solucao) - 1)
        self.__solucao.pop(index)
        i = 0
        while i + 1 in self.__solucao:
            i = randint(0, self.__dimension-1)
        pos = self.getBestPosition(i, self.__solucao)
        self.__solucao.insert(pos, i+1)

    def randomPerturb(self):
        index1 = randint(1, len(self.__solucao) - 1)
        index2 = index1
        while index1 == index2:
            index2 = randint(1, len(self.__solucao) - 1)
        aux = self.__solucao[index1]
        self.__solucao[index1] = self.__solucao[index2]
        self.__solucao[index2] = aux

    def ILS(self, repeat):
        self.buscaLocalRVND()

        k = 0
        while k < repeat:

            # Perturb
            j = 0
            while j < 4:
                self.addDropPerturb()
                j += 1

            self.__dist = self.calculateDist(self.__solucao)
            # Local Search
            self.buscaLocalRVND()
            k += 1

    def graspRVND(self, repeat, m):
        cont = 0
        currentDist = 0
        currentSol = []
        while(cont < repeat):
            self.__solucao = []
            self.findSolutionRandomHVMP(self.__n_pontos ,m)
            # self.findSolutionRandomHVMP2(m) # Semi random
            self.buscaLocalRVND()
            cont += 1
            if self.__dist < currentDist or currentDist == 0:
                currentDist = self.__dist
                currentSol = self.__solucao.copy()

        self.__solucao = currentSol.copy()
        self.__dist = currentDist

    """ Plotagem de solução """

    def plotar(self, plt):
        plt.show()

    def plotSol(self, sol, ax, color):

        # Prepara os pontos pertencentes a solução para inserir no gráfico
        x = []
        y = []
        for ponto in sol:
            x.append(ponto.getX())
            y.append(ponto.getY())
        # Plota os pontos pertencentes a solução no gráfico
        ax.plot(x, y, marker='o', color=color)

        # Enumera todos os pontos do gráfico de acordo com seus respectivos numeros
        for ponto in sol:
            if ponto.getNumero() == 1:
                plt.text(ponto.getX(), ponto.getY(), str(
                    ponto.getNumero()), fontsize='large')
            else:
                plt.text(ponto.getX(), ponto.getY(), str(
                    ponto.getNumero()), fontsize='medium')

    def plotAllPoints(self, ax):
        # Prepara os demais pontos para inserir no gráfico
        x = []
        y = []
        for ponto in self.__lista_de_pontos:
            x.append(ponto.getX())
            y.append(ponto.getY())

        # Plota os demais pontos no gráfico
        ax.scatter(x, y, marker='o')

    def createSol(self):
        solution = []
        for i in self.__solucao:
            solution.append(self.__lista_de_pontos[i-1])
        return solution

    def plotarSolucao(self, nome_do_arquivo):

        # Define o tamanho do gráfico a ser gerado
        fig, ax = plt.subplots(figsize=(10, 6))

        solution = self.createSol()

        self.plotAllPoints(ax)

        self.plotSol(solution, ax, 'red')

        # Configura o titulo do gráfico
        titulo = 'Solução da ' + self.__solType + ' para ' + \
            nome_do_arquivo + '\nDistância Total k = ' + str(self.__dist)
        ax.set(title=titulo, xlabel="Coordenadas x", ylabel="Coordenadas y")

        # Salva o gráfico como pdf no diretório do projeto
        posFormat = nome_do_arquivo.find('.')

        nome = 'Solução  para' + nome_do_arquivo[:posFormat] + '.pdf'
        plt.savefig(nome, format='pdf')
        self.plotar(plt)
        return plt


""" Funções auxiliares das metaheurísticas """


def randomizeLocalSearchs():
    localSearchs = []
    availableValues = [1, 2, 3]
    while len(availableValues) != 0:
        newInsert = randint(0, len(availableValues) - 1)
        localSearchs.append(availableValues.pop(newInsert))

    return localSearchs


def hashPerturb(i):
    return (i/25) + 1
