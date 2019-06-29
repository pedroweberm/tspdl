import random
import math
import numpy as np
import time
import sys

def parse_file(fileName):
    with open(fileName, "r") as f:
        lines = f.readlines()
        for line in lines: 
            line = line.replace("\n", "")
            print(line)

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

    averageCost = totalCost/pop.len()

def evaluate(c, x):
    cost = 0
    for i in range(0, x.len()):
        for j in range(0, c.len()):
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
    parse_file("instances/bayg29_10_1.dat")
    totalInitialCosts = 0
    totalFinalCosts = 0
    initialPop = []
    costs = []
    for i in range(0, 9):
        initialCost = evaluate(costs, generate_initial_pop(initialPop)["x"])
        totalInitialCosts = totalInitialCosts + initialCost
        finalCost = evaluate(costs, genetic_alg(initialPop)["x"])
        totalFinalCosts = totalFinalCosts + finalCost

    averageInitialCost = totalInitialCosts/len(initialPop)
    averageFinalCost = totalFinalCosts/len(initialPop)
