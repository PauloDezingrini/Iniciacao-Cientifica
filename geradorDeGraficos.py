from TSPfile import TSPfile
from solution import *
from pathlib import Path

def gerarGraficoPCV(fileName):
    files_folder = Path('C:/Users/Paulo Dezingrini/Documents/Codes/Python/Iniciacao-Cientifica/Instâncias/')
    file = files_folder / fileName
    file = TSPfile(file)
    sol = Solution(file.getDimension(),file.getList(),file.getMatriz(),file.getDimension())
    sol.graspRVND(100,4)
    solCopy = sol.getSolution()
    solCopy.append(1);
    sol.setSolution(solCopy)
    sol.plotarSolucao(fileName)

def gerarGraficoPCVtoBurma14():
    files_folder = Path('C:/Users/Paulo Dezingrini/Documents/Codes/Python/Iniciacao-Cientifica/Instâncias/')
    file = files_folder/'burma14.tsp'
    file = TSPfile(file)
    sol = Solution(file.getDimension(),file.getList(),file.getMatriz(),file.getDimension())
    newSol = [10,9,11,8,13,7,5,6,12,14,4,3,2,1,10]
    sol.setSolution(newSol)
    sol.plotarSolucao('burma14')

gerarGraficoPCVtoBurma14()

