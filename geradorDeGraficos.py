from TSPfile import TSPfile
from solution import *
from pathlib import Path

def getSolutionInstance(fileName):
    files_folder = Path('C:/Users/Paulo Dezingrini/Documents/Codes/Python/Iniciacao-Cientifica/Instâncias/')
    file = files_folder / fileName
    file = TSPfile(file)
    sol = Solution(file.getDimension(),file.getList(),file.getMatriz(),file.getDimension())
    return sol

def gerarGraficoPCV(fileName):
    sol = getSolutionInstance('burma14.tsp')
    sol.graspRVND(100,4)
    solCopy = sol.getSolution()
    solCopy.append(1);
    sol.setSolution(solCopy)
    sol.plotarSolucao(fileName)

def gerarGraficoPCVtoBurma14():
    sol = getSolutionInstance('burma14.tsp')
    newSol = [10,9,11,8,13,7,5,6,12,14,4,3,2,1,10]
    sol.setSolution(newSol)
    sol.plotarSolucao('burma14')

def gerarGraficoOpenPCVtoBurma14():
    sol = getSolutionInstance('burma14.tsp')
    newSol = [1,2,10,11,9,8,13,7,6,12,14,3,4,5]
    sol.setSolution(newSol)
    sol.plotarSolucao('burma14')

def gerarGraficoSubSetTourPCVtoBurma14():
    sol = getSolutionInstance('burma14.tsp')
    newSol = [10,9,11,8,7,6,12,14,2,1,10]
    sol.setSolution(newSol)
    sol.plotarSolucao('burma14')

def gerarGraficoSubSetTourOpenPCVtoBurma14():
    sol = getSolutionInstance('burma14.tsp')
    newSol =  [1,2,10,11,9,8,13,7,6,12]
    sol.setSolution(newSol)
    sol.plotarSolucao('burma14')


gerarGraficoSubSetTourOpenPCVtoBurma14()