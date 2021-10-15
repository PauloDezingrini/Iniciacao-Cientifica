from ponto import *
from math import sqrt,cos,acos,pi

class TSPfile(object):
    def __init__(self,fileName):
        self.__fileName = fileName
        self.__list = []
        self.__matriz = []
        self.__edge_type = ''
        self.__edge_format = ''
        self.read()

    def getList(self):
        #Gera uma copia e retorna a copia
        lista = self.__list[:]
        return lista

    def getMatriz(self):
        #Gera uma copia e retorna a copia
        matriz = self.__matriz[:]
        return matriz


    def read(self):
        file = open(self.__fileName,'r')
        lerCoord = False
        while True:
            str = file.readline()
            if str == "EOF" or str == "EOF\n":
                break
            if("EDGE_WEIGHT_TYPE:" in str):
                self.__edge_type = str[18:]
            if "EDGE_WEIGHT_FORMAT:" in str:
                self.__edge_format = str[20:]
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
                self.__list.append(newPonto)
            # Começa a leitura a partir da linha que ele encontra um dos textos abaixo.
            if ("NODE_COORD_SECTION\n" in str or "DISPLAY_DATA_SECTION\n" in str):
                lerCoord = True
        #A partir do edge weight type define qual será o método de leitura ou calculo da matriz de distâncias
        if(self.__edge_type=="EXPLICIT\n"):
            self.__matriz = self.lerMatriz()
        elif "EUC_2D\n" in self.__edge_type or "EUC_3D\n" in self.__edge_type:
            self.__matriz = self.calcularDistanciasEuclidianas()
        elif self.__edge_type == "GEO\n" : 
            self.__matriz = self.calcularDistanciasGeograficas()
        file.close()

    #Caso a matriz seja fornecida , realiza a leitura e caso não seja uma matriz quadrada , a ajusta para fazer com que ela se torne uma
    def lerMatriz(self):
        file = open(self.__fileName,'r')
        matriz = []
        readDists = False
        while True:
            str = file.readline()
            if (str == "NODE_COORD_SECTION\n" or str =="DISPLAY_DATA_SECTION\n"):
                break
            if readDists:
                aux = []
                str = str.split(" ")
                str = remove_values_from_list(str," ")
                str = remove_values_from_list(str,"")
                str[-1] = str[-1].strip('\n')
                for i in range(len(str)):
                    aux.append(int(str[i]))
                matriz.append(aux)
            if("EDGE_WEIGHT_SECTION" in str):
                readDists = True
        file.close()
        if "FULL_MATRIX" not in self.__edge_format:
            if "UPPER_ROW " in self.__edge_format or "LOWER_ROW" in str:
                return ajustarMatriz(matriz,1)
            else:
                return ajustarMatriz(matriz,0)
        else:
            return matriz
    
    def calcularDistanciasEuclidianas(self):
        matrizDeDistancias = []
        for i in range(len(self.__list)):
            linha = []
            for j in range(len(self.__list)):
                if(i==j):
                    linha.append(0)
                else:
                    ponto1 = self.__list[i]
                    ponto2 = self.__list[j]
                    x1 = ponto1.getX()
                    y1 = ponto1.getY()
                    x2 = ponto2.getX()
                    y2 = ponto2.getY()
                    dist = sqrt((x2 - x1)**2 + (y2  - y1)**2)
                    linha.append(dist)
            matrizDeDistancias.append(linha)
        return matrizDeDistancias
    
    def calcularDistanciasGeograficas(self):
        matrizDistancias = []
        RRR = 6378.388  
        for i in range(len(self.__list)):
            linha = []
            for j in range(len(self.__list)):
                if i==j:
                    linha.append(0)
                else:
                    ponto1 = self.__list[i]
                    ponto2 = self.__list[j]
                    lat1 , long1 = calcularLatitudeLongitude(ponto1)
                    lat2 , long2 = calcularLatitudeLongitude(ponto2)
                    q1 = cos(long1 - long2)
                    q2 = cos(lat1 - lat2)
                    q3 = cos(lat1 + lat2)
                    dist = (RRR*acos(0.5*((1.0+q1)*q2) - (1.0-q1)*q3) + 1.0)
                    linha.append(dist)
            matrizDistancias.append(linha)
        return matrizDistancias



#Funções auxiliares

# Remove um elemento qualquer de uma lista , é necessário já que ao quebrar a linha para obter os 3 valores(número do ponto , coord x ,coord y)
# sobra umas strings vazias e espaços que são delatados através desta função
def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

# Dada uma matriz triangular superior ajusta a matriz transformando-a em uma matriz quadrada completa
def ajustarMatriz(matriz,type):
    size = set(range(len(matriz) + type))
    matriz2 = [[0 if i ==j else matriz[i][j-i-1] if j>i else matriz[j][i-j-1] for j in size] for i in size]
    return matriz2

def calcularLatitudeLongitude(ponto):
    deg = round(ponto.getX())
    min = ponto.getX() - deg
    latitude = pi * (deg + 5.0*min/3.0)/180.0
    deg = round(ponto.getY())
    min = ponto.getY() - deg
    longitude = pi * (deg+5.0*min/3.0)/180.0
    return latitude,longitude

# Calcula a quantidade de elementos na matriz, usada apenas em testes.
def contarElementosMatriz(matriz):
    numeroElementos = 0
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            numeroElementos+=1
    print(numeroElementos)