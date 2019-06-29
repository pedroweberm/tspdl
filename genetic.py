import random
import math
import numpy as np
import time
import sys

costs = [[1,2,3,4,5],[5,4,3,2,1],[1,3,2,4,5],[5,2,1,3,4],[3,5,2,4,1],[1,2,3,4,5],[5,4,3,2,1],[1,3,2,4,5],[5,2,1,3,4],[3,5,2,4,1]]
demands = [0,1,1,1,1,1,1,1,1,1]
drafts = [9,1,9,9,9,8,9,9,2,9]
n = 10
seed = 5


def parse_file(fileName):
    with open(fileName, "r") as f:
        num_line = 0
        global n
        global costs
        global demands
        global drafts
        n = fileName.split("_")[0]
        n = n.replace("pcb", "")
        n = n.replace("bayg", "")
        n = n.replace("gr", "")
        n = n.replace("KroA", "")
        n = n.replace("ulysses", "")
        n = int(n)

        lines = f.readlines()
        if fileName[:3] == "pcb" or fileName[:4] == 'KroA':
            costs = [[0] * int(n) for i in range(int(n))]
            for line in lines:
                if num_line >= 1 and num_line <= 1 + (int(n)-1):
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(int(n)):
                        costs[num_line-1][i] = (int(numeros[i]))
                if num_line == 1 + (int(n)-1) + 1:
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(len(numeros) - 1):
                        demands.append(int(numeros[i]))
                if num_line == 1 + (int(n)-1) + 2:
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(len(numeros) - 1):
                        drafts.append(int(numeros[i]))
                num_line += 1
        else:
            costs = [[0] * int(n) for i in range(int(n)-1)]
            for line in lines:
                if num_line >= 16 and num_line < 16 + (int(n)-1):
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(int(n)):
                        costs[num_line-16][i] = (int(numeros[i]))
                if num_line == 16 + (int(n)-1) + 8:
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(len(numeros) - 1):
                        demands.append(int(numeros[i]))
                if num_line == 16 + (int(n)-1) + 11:
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(len(numeros) - 1):
                        drafts.append(int(numeros[i]))
                num_line += 1
        # for line in costs:
        #    print(line)
        # print(demands)
        # print(drafts)

def validateSolution(x, y):

    global demands
    global costs
    global n
    global drafts
    
    rest1 = 1;
    #Primeiro conjunto de restricoes: soma de todas colunas e igual a 1
    for j in range(0, n):
        rest1 = 0
        for i in range(0, n):
            rest1 += x[i][j]
        if (rest1 != 1):
            print("SOLUÇÃO NÃO É VÁLIDA: Soma alguma coluna não é igual a 1")
            return False
    
    rest2 = 1;
    #Segund0 conjunto de restricoes: soma de todas linhas e igual a 1
    for i in range(0, n):
        rest2 = 0
        for j in range(0, n):
            rest2 += x[i][j]
        if (rest2 != 1):
            print("SOLUÇÃO NÃO É VÁLIDA: Soma de alguma linha não é igual a 1")
            return False

    rest31 = 0
    rest32 = 0
    #Terceiro conjunto de restricoes: demanda dos portos e atendidas
    for j in range(1, n):
        rest31 = 0
        rest32 = 0
        for i in range(0, n):
            rest31 += y[i][j]
        for i in range(0, n):
            rest32 += y[j][i]
        if ((rest31 - rest32) != demands[j]):
            print("SOLUÇÃO NÃO É VÁLIDA: Demanda de todos portos não é atendida")
            return False
    
    rest41 = 0
    rest42 = 0
    #Quarto conjunto de restricoes: embarcacao sai da garagem carregada com toda demanda necessaria
    for j in range(0, n):
        rest41 += y[0][j]
    for i in range(0, n):
        rest42 += demands[i]
    
    if rest41 != rest42:
        print("SOLUÇÃO NÃO É VÁLIDA: Embarcação não sai suficientemente carregada (soma das demandas)")
        return false

    rest5 = 0
    #Quinto conjunto de restricoes: so retorna para o porto quando estiver vazio
    for i in range(0, n):
        rest5 += y[i][0]

    if rest5 != 0:
        print("SOLUÇÃO NÃO É VÁLIDA: Embarcação retorna para o porto com carga maior que 0")
        return False

    #Sexto conjunto de restricoes: limites de profundidade e implicacao
    for i in range(0, n):
        for j in range(0, n):
            if (y[i][j] < 0 || y[i][j] > drafts[j]*x[i][j]):
                print("SOLUÇÃO NÃO É VÁLIDA: Profundidade limite violada ou implicação de y e x violada")
                return False

    
def generate_initial_pop(initialPop, popSize):
    for i in range(0, popSize - 1):
        initialPop.append(generateIndividual())
    pass
    # return bestIndividual


def generateIndividual():
    global costs
    global demands
    global drafts
    global n
    global seed
    
    #random.seed(seed)

    x = [[0] * int(n) for i in range(int(n))]
    unvisited = range(1, n)
    validChoices = []
    solucao = []

    currentDraft = sum(demands)
    
    for i in  range(0, n-1):
        validChoices = []
        for j in range(0, len(unvisited)):
            if drafts[unvisited[j]] >= currentDraft:
                validChoices.append(unvisited[j])

        chosen = random.choice(validChoices)
        currentDraft = currentDraft - demands[chosen]
        unvisited.remove(chosen)
        solucao.append(chosen)

    print(solucao)


def evaluate_pop(pop, costs):
    totalCost = 0
    popCosts = []
    for individual in pop:
        individualCost = evaluate(costs, individual["x"])
        totalCost = totalCost + individualCost
        popCosts.append(individualCost)

    averageCost = totalCost/len(pop)


def evaluate(c, x):
    cost = 0
    for i in range(0, len(x)):
        for j in range(0, len(c)):
            cost = cost + x[i][j]*c[i][j]

    return cost


def select_individuals():
    pass


def reproduce():
    pass


def mutate():
    pass


def genetic_alg(initialPop):
    pass
    # return bestIndividual


def generate_neighbour():
    pass


if __name__ == '__main__':
    parse_file(sys.argv[1])
    totalInitialCosts = 0
    totalFinalCosts = 0
    initialPop = []
    global costs
    global demands
    global drafts
    global n

    #for i in range(0, 9):
    #    initialCost = evaluate(costs, generate_initial_pop(initialPop)["x"])
    #    totalInitialCosts = totalInitialCosts + initialCost
    #    finalCost = evaluate(costs, genetic_alg(initialPop)["x"])
    #    totalFinalCosts = totalFinalCosts + finalCost

    #averageInitialCost = totalInitialCosts/len(initialPop)
    #averageFinalCost = totalFinalCosts/len(initialPop)

    generateIndividual()
