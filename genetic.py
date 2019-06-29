import random
import math
import numpy as np
import time
import sys

costs = [[1,2,3,4,5],[5,4,3,2,1],[1,3,2,4,5],[5,2,1,3,4],[3,5,2,4,1],[1,2,3,4,5],[5,4,3,2,1],[1,3,2,4,5],[5,2,1,3,4],[3,5,2,4,1]]
demands = [0,1,1,1,1,1,1,1,1,1]
drafts = [9,1,9,9,9,9,9,9,9,9]
n = 10
seed = 50


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
    y = [[0] * int(n) for i in range(int(n))]
    
    solucaoValida = False
    while(not solucaoValida):
        currentDraft = sum(demands)
        unvisited = list(range(1, n)) 
        solucao = []
        for i in  range(0, n-1):
            validChoices = []
            for j in range(0, len(unvisited)):
                if drafts[unvisited[j]] >= currentDraft:
                    validChoices.append(unvisited[j])

            chosen = random.choice(validChoices)
            currentDraft = currentDraft - demands[chosen]
            unvisited.remove(chosen)
            solucao.append(chosen)
        solucaoValida = validateSolution(solucao)
    
    print(solucao)
    currentDraft = sum(demands) - demands[solucao[0]]
    for i in range(len(solucao)):
        if i >= 0 and i < len(solucao) - 1:
            x[solucao[i]][solucao[int(i)+1]] = 1
            y[solucao[i]][solucao[int(i)+1]] = currentDraft
        if i == 0:
            x[0][solucao[i]] = 1
            y[0][solucao[i]] = sum(demands)
        if i == len(solucao) - 1:
            x[solucao[i]][0] = 1
            y[solucao[i]][0] = currentDraft

        currentDraft = currentDraft - demands[solucao[i]]

def validateSolution(solution):
    return True

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
    #parse_file(sys.argv[1])
    #totalInitialCosts = 0
    #totalFinalCosts = 0
    #initialPop = []

    #for i in range(0, 9):
    #    initialCost = evaluate(costs, generate_initial_pop(initialPop)["x"])
    #    totalInitialCosts = totalInitialCosts + initialCost
    #    finalCost = evaluate(costs, genetic_alg(initialPop)["x"])
    #    totalFinalCosts = totalFinalCosts + finalCost

    #averageInitialCost = totalInitialCosts/len(initialPop)
    #averageFinalCost = totalFinalCosts/len(initialPop)

    generateIndividual()
