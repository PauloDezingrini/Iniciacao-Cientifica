class Ponto(object):
    def __init__(self,numero_do_ponto,coord_x,coord_y):
        self.__numero = int(numero_do_ponto)
        self.__x = float(coord_x)
        self.__y = float(coord_y)
    def getX(self):
        return self.__x
    def getY(self):
        return self.__y
    def getNumero(self):
        return self.__numero
