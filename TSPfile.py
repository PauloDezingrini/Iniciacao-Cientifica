from ponto import *
from math import sqrt,cos,acos,pi

class TSPfile(object):
    def __init__(self,fileName):
        self.__fileName = fileName
        self.__list = []
        self.__matriz = []
        self.__edge_type = ''
        self.__edge_format = ''
        self.__dimension = 0
        self.read()
    
    # Getters, geram uma cópia da lista/matriz e a retorna
    def getList(self):
        lista = self.__list[:]
        return lista

    def getMatriz(self):
        matrix = self.__matriz[:]
        return matrix

    def getDimension(self):
        return self.__dimension

    # Função de leitura principal
    def read(self):
        fileReaded = open(self.__fileName,'r')
        file = fileReaded.readlines()
        fileReaded.close()
        for i in range(len(file)):
            if "EOF" in file[i]:
                break
            if "EDGE_WEIGHT_TYPE" in file[i]:
                self.__edge_type = file[i][18:]
            if "EDGE_WEIGHT_FORMAT" in file[i]:
                self.__edge_format = file[i][20:]
            if "DIMENSION" in file[i]:
                str = file[i][11:]
                str = str.strip('\n')
                self.__dimension = int(str)
            if "EDGE_WEIGHT_SECTION" in file[i] :
                matrixIndex = i
            if "NODE_COORD_SECTION\n" in file[i] or "DISPLAY_DATA_SECTION\n" in file[i]:
                self.readPoints(file,i + 1)
        if "EXPLICIT\n" in self.__edge_type:
            self.readMatrix(file,matrixIndex + 1)
        elif "EUC_2D\n" in self.__edge_type or "EUC_3D\n" in self.__edge_type:
            self.__matriz = self.calcularDistanciasEuclidianas()
            pass
        elif "GEO\n" in self.__edge_type: 
            pass
            self.__matriz = self.calcularDistanciasGeograficas()
        elif "ATT\n" in self.__edge_type:
            pass
            self.__matriz = self.calcularDistanciasATT()

    # Funções de leitura especializadas
    def readPoints(self,file,index):
        while True:
            if "EOF" in file[index]:
                break
            str = stringToIntArray(file[index])
            newPonto = Ponto(str[0],str[1],str[2])
            self.__list.append(newPonto)
            index += 1
    
    def readMatrix(self,file,index):
        if "FULL_MATRIX" in self.__edge_format:
            self.__matriz = self.readMatrixFull_Upper(file,index,0)
        elif "UPPER_ROW" in self.__edge_format or "UPPER_DIAG_ROW" in self.__edge_format:
            self.__matriz = self.readMatrixFull_Upper(file,index,1)
        elif "LOWER_ROW" in self.__edge_format or "LOWER_DIAG_ROW" in self.__edge_format:
            self.__matriz = self.readMatrixLower(file,index)

    def readMatrixFull_Upper(self,file,index,step):
        if "UPPER_ROW" in self.__edge_format:
            count = self.__dimension - 1
        else:
            count = self.__dimension
        matrix = []
        str = stringToIntArray(file[index])
        while True:
            if "NODE_COORD_SECTION\n" in file[index] or "DISPLAY_DATA_SECTION\n" in file[index] or "EOF" in file[index]:
                break
            line = []
            if not str:
                index+=1
                str = stringToIntArray(file[index])
            for i in range(count):
                line.append(int(str[0]))
                str.pop(0)
                if not str:
                    index += 1
                    str = stringToIntArray(file[index])
                    # Não é necessário, está aqui por garantia
                    if (file[index] == "NODE_COORD_SECTION\n" or file[index] =="DISPLAY_DATA_SECTION\n" or "EOF" in file[index]):
                            break
            matrix.append(line)
            count -= step
        if "UPPER_ROW" in self.__edge_format:
            matrix = ajustarMatrizUpper(matrix,1)
        elif "UPPER_DIAG_ROW" in self.__edge_format:
            matrix = ajustarMatrizUpper2(matrix,0)
        return matrix

    def readMatrixLower(self,file,index):
        count = 1
        matrix = []
        str = stringToIntArray(file[index])
        while True:
            if "NODE_COORD_SECTION\n" in file[index] or "DISPLAY_DATA_SECTION\n" in file[index] or "EOF" in file[index]:
                break
            line = []
            if not str:
                index += 1
                str = stringToIntArray(file[index])
            for i in range(count):
                line.append(int(str[0]))
                str.pop(0)
                if not str:
                    index += 1
                    str = stringToIntArray(file[index])
                    # Não é necessário, está aqui por garantia
                    if (file[index] == "NODE_COORD_SECTION\n" or file[index] =="DISPLAY_DATA_SECTION\n" or "EOF" in file[index]):
                            break
            matrix.append(line)
            count += 1
        if "LOWER_ROW" in self.__edge_format:
            matrix = ajustarMatrizLower(matrix,1)
        elif "LOWER_DIAG_ROW" in self.__edge_format:
            matrix = ajustarMatrizLower(matrix,0)
        return matrix
    
    # Funções que calculam e geram a matriz de distâncias
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
    
    def calcularDistanciasATT(self):
        matrizDistancias = []
        for i in range(len(self.__list)):
            linha = []
            for j in range(len(self.__list)):
                if(i==j):
                    linha.append(0)
                else:
                    ponto1 = self.__list[i]
                    ponto2 = self.__list[j]
                    xd = ponto1.getX() - ponto2.getX()
                    yd = ponto1.getY() - ponto2.getY()
                    r = sqrt((xd**2 + yd**2)/10)
                    t = int(round(r))
                    if(t<r): 
                        linha.append(t + 1)
                    else:
                        linha.append(t)
            matrizDistancias.append(linha)
        return matrizDistancias

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

def stringToIntArray(str):
    str = str.strip('\n')
    str = str.split(" ")
    str = remove_values_from_list(str," ")
    str = remove_values_from_list(str,"")
    return str

# Remove um elemento qualquer de uma lista , é necessário já que ao quebrar a linha para obter os 3 valores(número do ponto , coord x ,coord y)
# sobra umas strings vazias e espaços que são delatados através desta função
def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

# Dada uma matriz triangular superior ajusta a matriz transformando-a em uma matriz quadrada completa
def ajustarMatrizUpper(matriz,type):
    size = set(range(len(matriz) + type))
    matriz2 = [[0 if i ==j else matriz[i][j-i-1] if j>i else matriz[j][i-j-1] for j in size] for i in size]
    return matriz2

def ajustarMatrizUpper2(matrix,type):
    matrix2 = []
    size = range(len(matrix) + type)
    for linha in size:
        line = []
        for coluna in size:
            # print("Linha: ",linha," - Coluna: ",coluna)
            if linha == coluna:
                line.append(0)
            elif linha > coluna:
                line.append(matrix[coluna][linha - coluna])
            else:
                line.append(matrix[linha][coluna - linha])
        matrix2.append(line)
    return matrix2

def ajustarMatrizLower(matrix,type):
    matrix2 = []
    size = range(len(matrix) + type)
    for i in size:
        line = []
        for j in size:
            if i==j:
                line.append(0)
            elif i < j:
                line.append(matrix[j][i])
            else:
                line.append(matrix[i][j])
        matrix2.append(line)
    return matrix2


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