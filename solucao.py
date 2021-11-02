from os import pipe
from typing import Counter, Sized
from ponto import *
import random

import matplotlib.pyplot as plt

from mip import Model, xsum, minimize, BINARY

class Solucao(object):
    def __init__(self,numero_de_pontos,lista_de_pontos,matriz_de_distancias):
        self.__pontos = []
        self.__distTotal = 0
        self.__numero_de_pontos = int(numero_de_pontos)
        self.__lista_de_pontos = lista_de_pontos
        self.__matriz_de_distancias = matriz_de_distancias
        self.__solType = ""

    def __str__(self):
        for ponto in self.__pontos:
            print("Ponto de numero:",ponto.getNumero()," com coordenadas: ",ponto.getX()," , ",ponto.getY())
        return "Com uma distancia total de " + str(self.__distTotal)

    def getPontos(self):
        print(self.__distTotal)

    def calcularDistTotal(self):
        distTotal = 0
        for i in range(len(self.__pontos) - 1):
            n1 = self.__pontos[i]
            n2 = self.__pontos[i + 1]
            # O - 1 é devido ao fato da lista começar em 0 , não em 1 , portanto o ponto 1 está na posição 0 , o ponto 2 na posição e por ai vai 
            distTotal += self.__matriz_de_distancias[n1 - 1][n2 - 1]
        self.__distTotal = round(distTotal,2)


    def encontrarSolucaoRandomica(self):
        # Como a leitura é feita de forma a seguir o numero dos pontos e o primeiro ponto de toda solução tem que ser o ponto 1
        # Podemos fazer essa atribuição diretamente com a posicao 0 da lista de pontos
        self.__pontos.append(self.__lista_de_pontos[0])
        self.__lista_de_pontos.pop(0)
        # Enquanto o tamanho da solução(__pontos) for menor que o numero de pontos pedidos ele escolhe uma posicao aleatoaria do array
        # Entao adiciona essa solucao ao vetor __pontos e deleta do vetor auxiliar para evitar repeticoes
        while(len(self.__pontos)<self.__numero_de_pontos):
            index = random.randint(0,len(self.__lista_de_pontos)-1)
            self.__pontos.append(self.__lista_de_pontos[index])
            self.__lista_de_pontos.pop(index)
        self.calcularDistTotal()
        self.__solType = "Randomica"

    # Método que retorna a posição do ponto mais próximo a um ponto determinado na chamada da função(index) ou ao ultimo ponto soluçao se inder for -1
    # Parametro extra lista é utilizado na heurística do vizinho mais próximo com escolhas aleátorias
    def encontrarPontoMaisProximo(self,lista,size,index):
        # Size é passado como paramentro simplesmente para evitar fazer a operaçao len(lista_de_pontos) repetidas vezes 
        # Representa o ponto de saída de determinado trecho da rota
        saiDe = self.__pontos[index] - 1 
        menorDist = 0
        for i in range(size):
            if((self.__matriz_de_distancias[saiDe][i]<=menorDist) or (menorDist==0)):
                # Somente escolhe como ponto mais proximo , pontos que não estejam na solução
                if (i+1) not in self.__pontos and (i+1) not in lista:
                    menorDist = self.__matriz_de_distancias[saiDe][i]
                    novoPonto = i
        return novoPonto

    def encontrarSolucaoVizinhoProximo(self): 
        self.__pontos.append(1)
        # A matriz_de_distancias possui dimensão size X size , como precisamos percorrer linhas/colunas da matriz o valor size já
        # foi definido previamente
        size = len(self.__matriz_de_distancias[0])
        while(len(self.__pontos) < self.__numero_de_pontos):
            # Como queremos encontrar o ponto mais proximo do ultimo inserido no array , basta passar -1 como ultimo paramentro
            pos = self.encontrarPontoMaisProximo(self.__pontos,size,-1)
            self.__pontos.append(pos+1)
        self.__solType = "HVMP"
        self.calcularDistTotal()

    def encontrarSolucaoVMPA(self,percentual):
        size = len(self.__matriz_de_distancias[0])
        # Quantidade de pontos mais proximos que será disponibilizado para escolha
        m = int(round(max(1,percentual*size)))
        # Inserção do ponto inicial
        self.__pontos.append(1)
        cont = 1
        while(cont < self.__numero_de_pontos):
            maisProximos = []
            index = 0
            while(index < m):
                pos = self.encontrarPontoMaisProximo(maisProximos,size,-1)
                maisProximos.append(pos+1)
                index += 1
            pos = random.randint(0,m-1)
            self.__pontos.append(maisProximos[pos])
            cont+=1
        self.__solType = "HVMPA"
        self.calcularDistTotal()

    def encontrarSolucaoInsercaoMaisBarata(self):
        size = len(self.__lista_de_pontos)
        # Adição dps pontos iniciais a solução
        self.__pontos.append(self.__lista_de_pontos[0])
        # print(self.__pontos[-1].getNumero(),end=",")
        self.encontrarPontoMaisProximo(size,-1)
        # print(self.__pontos[-1].getNumero(),end=",")
        self.encontrarPontoMaisProximo(size,-1)
        # print(self.__pontos[-1].getNumero(),end=",")
        # count representa o número de pontos ja adicionados a soluçao
        count = 3
        # Enquanto o número de pontos da solução for menor que a quantidade de pontos que a solução tem que ter(k)
        while(count < self.__numero_de_pontos):
            menorDist = -1
            for i in range(count): # Percorre a solução
                for j in range(len(self.__lista_de_pontos)): # Percorre a lista de pontos
                    if self.__lista_de_pontos[j] not in self.__pontos: # Garante que o ponto j não está na solução
                        indexJ = self.__lista_de_pontos[j].getNumero() - 1
                        if i == count - 1:
                            # O indice do ponto é pego dessa maneira , pq queremos o indice do ponto na matriz e como está sendo deletado
                            # da lista de ponto , os pontos utilizados os indices podem não corresponder
                            dist = self.__matriz_de_distancias[self.__pontos[i].getNumero() - 1][indexJ]
                        else:
                            dist = self.__matriz_de_distancias[self.__pontos[i].getNumero() - 1][indexJ] + self.__matriz_de_distancias[indexJ][self.__pontos[i + 1].getNumero() - 1] - self.__matriz_de_distancias[self.__pontos[i].getNumero() - 1][self.__pontos[i+1].getNumero() - 1]
                        if dist < menorDist or menorDist==-1:
                            menorDist = dist
                            after  = i + 1
                            where = j
            count += 1
            # Insere na posição after o ponto que resultou na menor dist que está na posição where e então , por questões de eficiencia
            # Exclui esse ponto da lista
            self.__pontos.insert(after,self.__lista_de_pontos[where])
            # print(self.__lista_de_pontos[where].getNumero(),end=",")
            self.__lista_de_pontos.pop(where)
            # A distância não é atualizada pq o método calcularDistTotal() já realiza este papel
        self.__solType = "HIMB"
        self.calcularDistTotal()

    def encontrarSolucaoModelo(self):
        self.__solType = "Modelo"
        # size1 é utilizado em restrições que iniciam desde o primeiro ponto , enquanto o size2 exclui esse ponto
        size1 = set(range(len(self.__matriz_de_distancias[0]) -1))
        size2 = set(range(1,len(self.__matriz_de_distancias[0])-1))

        model = Model()
        x = [[model.add_var(var_type=BINARY) for j in size1] for i in size1]
        y = [model.add_var(var_type=BINARY) for i in size1]
        F = [[model.add_var() for i in size1] for j in size1]

        model.objective = minimize(xsum(self.__matriz_de_distancias[i][j]*x[i][j] for i in size1 for j in size1))

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
        model += xsum(y[i] for i in size1) == self.__numero_de_pontos

        # Restriçao 7
        for i in size2:
            model += (xsum(F[h][i]for h in size1) - xsum(F[i][j] for j in size1)) == y[i]
        # Restriçao 8
        for i in size1:
            for j in size1:
                model+= F[i][j] <= (self.__numero_de_pontos - 1)*x[i][j]
        # Restriçao 9 : 
        for j in size1:
            model += (xsum(x[i][j] for i in size1) - xsum(x[j][h] for h in size2)) <=1

        model.optimize(max_seconds=3600)
        pontos_utilizados = []
        if model.num_solutions:
            self.__distTotal = model.objective_value
            posSaida = 0
            pontos_utilizados.append(0)
            while True:
                for i in size2:
                    if(x[posSaida][i].x >= 0.90 and i not in pontos_utilizados):
                        pontos_utilizados.append(i)
                        posSaida = i
                        break
                if(len(pontos_utilizados) == self.__numero_de_pontos):
                    break
            for i in range(self.__numero_de_pontos):
                self.__pontos.append(pontos_utilizados[i] + 1)

    def plotarSolucao(self,nome_do_arquivo):

        solution = []
        for i in self.__pontos:
            solution.append(self.__lista_de_pontos[i-1])
        # Prepara os pontos pertencentes a solução para inserir no gráfico
        x = []
        y = []
        for ponto in solution:
            x.append(ponto.getX())
            y.append(ponto.getY())
        # Prepara os demais pontos para inserir no gráfico

        x1 = []
        y1 = []
        for ponto in self.__lista_de_pontos:
            x1.append(ponto.getX())
            y1.append(ponto.getY())
        
        # Define o tamanho do gráfico a ser gerado
        fig , ax = plt.subplots(figsize=(10,6))
        #Plota os demais pontos no gráfico
        ax.scatter(x1,y1,marker = 'o')
        # Plota os pontos pertencentes a solução no gráfico
        ax.plot(x,y,marker = 'o',color='red')

        # Configura o titulo do gráfico
        titulo = 'Solução da '+ self.__solType + ' para ' + nome_do_arquivo + '\nDistância Total k = ' + str(self.__distTotal)
        ax.set(title = titulo,xlabel = "Coordenadas x",ylabel = "Coordenadas y")

        # Enumera todos os pontos do gráfico de acordo com seus respectivos numeros
        for ponto in solution:
            if ponto.getNumero() == 1:
                plt.text(ponto.getX(),ponto.getY(),str(ponto.getNumero()),fontsize = 'large')
            else : 
                plt.text(ponto.getX(),ponto.getY(),str(ponto.getNumero()),fontsize = 'medium')

        # Salva o gráfico como pdf no diretório do projeto
        posFormat = nome_do_arquivo.find('.')
        nome  = 'Solução da '+ self.__solType + ' para ' + nome_do_arquivo[:posFormat] + '.pdf'
        # plt.savefig(nome,format = 'pdf')
        plt.show()
        return plt

