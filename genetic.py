import random
import math
import numpy as np
import time
import sys

def parse_file(fileName, costs, drafts, demands):
    with open(fileName, "r") as f:
        num_line = 0
        n = fileName.split("_")[0]
        n = n.replace("pcb", "")
        n = n.replace("bayg", "")
        n = n.replace("gr", "")
        n = n.replace("KroA", "")
        n = n.replace("ulysses", "")

        

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
                num_line+=1
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
                num_line+=1
        #for line in costs:
        #    print(line)
        #print(demands)
        #print(drafts)

def generate_initial_pop(initialPop):
    pass
    #return bestIndividual


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
    #return bestIndividual


def generate_neighbour():
    pass

if __name__ == '__main__':
    costs = []
    drafts = []
    demands = []
    parse_file(sys.argv[1], costs, drafts, demands)
    totalInitialCosts = 0
    totalFinalCosts = 0
    initialPop = []
    
    for i in range(0, 9):
        initialCost = evaluate(costs, generate_initial_pop(initialPop)["x"])
        totalInitialCosts = totalInitialCosts + initialCost
        finalCost = evaluate(costs, genetic_alg(initialPop)["x"])
        totalFinalCosts = totalFinalCosts + finalCost

    averageInitialCost = totalInitialCosts/len(initialPop)
    averageFinalCost = totalFinalCosts/len(initialPop)
