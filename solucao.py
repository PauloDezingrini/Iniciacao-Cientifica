from ponto import *
import random

import matplotlib.pyplot as plt

from mip import Model, xsum, minimize, BINARY

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

    def encontrarSolucaoVizinhoProximo(self,lista_de_pontos,matriz_de_distancias): 
        pontos_utilizados = []
        pontos_utilizados.append(0)

        # A matriz_de_distancias possui dimensão size X size , como precisamos percorrer linhas/colunas da matriz o valor size já
        # foi definido previamente
        size = len(lista_de_pontos)
        posNovoPonto = 0
        while(len(pontos_utilizados) < self.__numero_de_pontos):
            # Representa o ponto de saída de determinado trecho da rota
            saiDe = pontos_utilizados[-1]
            menorDist = 0
            for i in range(size):
                if((matriz_de_distancias[saiDe][i]<=menorDist) or (menorDist==0)):
                    if i not in pontos_utilizados:
                        menorDist = matriz_de_distancias[saiDe][i]
                        posNovoPonto = i

            pontos_utilizados.append(posNovoPonto)

        for i in range(self.__numero_de_pontos):
            self.__pontos.append(lista_de_pontos[pontos_utilizados[i]])

    def encontrarSolucaoModelo(self,lista_de_pontos,matriz_de_distancias):
        model = Model()
        x = [[model.add_var(var_type=BINARY) for j in lista_de_pontos] for i in lista_de_pontos]
        y = [model.add_var(var_type=BINARY) for i in lista_de_pontos]
        F = [[model.add_var() for i in lista_de_pontos] for j in lista_de_pontos]

        # size1 é utilizado em restrições que iniciam desde o primeiro ponto , enquanto o size2 exclui esse ponto
        size1 = set(range(len(lista_de_pontos)))
        size2 = set(range(1,len(lista_de_pontos)))

        model.objective = minimize(xsum(matriz_de_distancias[i][j]*x[i][j] for i in size1 for j in size1))

        # Restricoes 2 e 3
        model += xsum(x[0][j] for j in size1) == 1
        model += xsum(x[i][0] for i in size1) == 0

        # Restricoes 4 e 5
        for j in size1:
            model += xsum(x[i][j] for i in size1 if i!=j) <= 1

        for i in size1:
            model += xsum(x[i][j] for j in size1 if i!=j) <= 1
        
        # Restriçao 6
        model += xsum(y[i] for i in size1) == self.__numero_de_pontos

        # Restriçao 7
        for i in size2:
            model += (xsum(F[h][i]for h in size1) - xsum(F[i][j] for j in size1)) == y[i]
        # Restriçao 8
        for i in size1:
            for j in size1:
                model+= F[i][j] <= (self.__numero_de_pontos - 1)*x[i][j]
        # Restriçao 9
        for j in size1:
            model += (xsum(x[i][j] for i in size1) - xsum(x[j][h] for h in size2)) <=1

        model.optimize()

        if model.num_solutions:
            self.__distTotal = model.objective_value
            nc = 0
            print(nc)
            print('\n')
            while True:
                nc = [i for i in size1 if x[nc][i] >= 0.99][0]
                print(nc)
                print('\n')
                self.__pontos.append(lista_de_pontos[nc])
                if nc==0:
                    break


        pass

    def plotarSolucao(self,nome_do_arquivo,lista_de_pontos):
        # Prepara os pontos pertencentes a solução para inserir no gráfico
        x = []
        y = []
        for ponto in self.__pontos:
            x.append(ponto.getX())
            y.append(ponto.getY())
        # Prepara os demais pontos para inserir no gráfico

        x1 = []
        y1 = []
        for ponto in lista_de_pontos:
            x1.append(ponto.getX())
            y1.append(ponto.getY())
        
        # Define o tamanho do gráfico a ser gerado
        fig , ax = plt.subplots(figsize=(10,6))
        #Plota os demais pontos no gráfico
        ax.scatter(x1,y1,marker = 'o')
        # Plota os pontos pertencentes a solução no gráfico
        ax.plot(x,y,marker = 'o',color='red')

        # Configura o titulo do gráfico
        titulo = 'Solução para ' + nome_do_arquivo + '\nDistância Total k = ' + str(self.__distTotal)
        ax.set(title = titulo,xlabel = "Coordenadas x",ylabel = "Coordenadas y")

        # Enumera todos os pontos do gráfico de acordo com seus respectivos numeros
        for ponto in self.__pontos:
            if ponto.getNumero() == 1:
                plt.text(ponto.getX(),ponto.getY(),str(ponto.getNumero()),fontsize = 'x-large')
            else : 
                plt.text(ponto.getX(),ponto.getY(),str(ponto.getNumero()),fontsize = 'x-small')

        # Salva o gráfico como pdf no diretório do projeto
        posFormat = nome_do_arquivo.find('.')
        nome  = 'Solução para ' + nome_do_arquivo[:posFormat] + '.pdf'
        plt.savefig(nome,format = 'pdf')
        plt.show()
        return plt
        