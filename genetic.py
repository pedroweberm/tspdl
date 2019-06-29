import random
import math
import numpy as np
import time
import sys


def generate_initial_pop(initialPop):

    return bestIndividual


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


def reproduce():


def mutate():


def genetic_alg(initialPop):

    return bestIndividual


def generate_neighbour():


def learn():
    totalInitialCosts = 0
    totalFinalCosts = 0
    initialPop = []
    for i in range(0, 9):
        initialCost = evaluate(costs, generate_initial_pop(initialPop)["x"])
        totalInitialCosts = totalInitialCosts + initialCost
        finalCost = evaluate(costs, genetic_alg(initialPop)["x"])
        totalFinalCosts = totalFinalCosts + finalCost

    averageInitialCost = totalInitialCosts/initialPop.len()
    averageFinalCost = totalFinalCosts/initialPop.len()
