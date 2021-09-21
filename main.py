# -*- coding: utf-8 -*-

from ponto import *
from solucao import *
from math import sqrt

# Remove um elemento qualquer de uma lista , é necessário já que ao quebrar a linha para obter os 3 valores(número do ponto , coord x ,coord y)
# sobra umas strings vazias e espaços que são delatados através desta função
def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]


# Calcula a matriz de distancias e a retorna. A matriz de distancias será n x n , onde n é o numero de pontos lidos a partir do arquivo
def calcularDistancias(lista_de_pontos):
    matrizDeDistancias = []
    for i in range(len(lista_de_pontos)):
        linha = []
        for j in range(len(lista_de_pontos)):
            if(i==j):
                linha.append(0)
            else:
                ponto1 = lista_de_pontos[i]
                ponto2 = lista_de_pontos[j]
                x1 = ponto1.getX()
                y1 = ponto1.getY()
                x2 = ponto2.getX()
                y2 = ponto2.getY()
                dist = sqrt((x2 - x1)**2 + (y2  - y1)**2)
                linha.append(dist)
        matrizDeDistancias.append(linha)
    return matrizDeDistancias

# Calcula a quantidade de elementos na matriz, usada apenas em testes.
def contarElementosMatriz(matriz):
    numeroElementos = 0
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            numeroElementos+=1
    print(numeroElementos)



# Responsável por fazer a leitura do arquivo , falta implementar os casos de entradas de dados especiais. Como quando recebe direto a matriz
# de distâncias
def realizarLeitura(arquivo_a_ser_lido):
    # file = open('a280.txt','r')
    file = open(arquivo_a_ser_lido,'r')
    str = "a"
    lista = []

    lerCoord = False
    while True:
        str  = file.readline()
        if str == "EOF":
            break
        if lerCoord:
            # Separa a linha a partir dos espaçoes e então remove os espaços vazios que restarem devido a espaços seguidos e strings "" que 
            # estavam sobrando no array
            aux = str.split(" ")
            filtered = remove_values_from_list(aux," ")
            filtered = remove_values_from_list(filtered,"")
            # Remove os \n do final do ultimo valor de cada linha
            filtered[2] = filtered[2].strip('\n')
            # Adiciona para a lista o array [numero_do_ponto,x,y]
            newPonto = Ponto(filtered[0],filtered[1],filtered[2])
            lista.append(newPonto)
        # Começa a leitura a partir da linha que ele encontra um dos textos abaixo.
        if str == "NODE_COORD_SECTION\n" or str =="DISPLAY_DATA_SECTION\n":
            lerCoord = True
    file.close()
    return lista


while True:

    arquivo_a_ser_lido = input("Digite o nome do arquivo que será lido: ")

    lista_de_pontos = realizarLeitura(arquivo_a_ser_lido)

    matrizDistancias = calcularDistancias(lista_de_pontos)

    numero_de_pontos = int(input("Digite o numero de pontos que terá a solução: "))

    solucao = Solucao(numero_de_pontos)
    # solucao.encontrarSolucaoRandomica(lista_de_pontos)
    solucao.encontrarSolucaoVizinhoProximo(lista_de_pontos,matrizDistancias)
    solucao.calcularDistTotal(matrizDistancias)
    print(solucao)
    solucao.plotarSolucao(arquivo_a_ser_lido,lista_de_pontos)

    continuar = input("Deseja realizar outra leitura? (S p/ sim) (N p/ não)"    )

    if continuar == 'N':
        break
