import random
import math
import numpy as np
import time
import sys
import statistics

# costs = [[1,2,3,4,5],[5,4,3,2,1],[1,3,2,4,5],[5,2,1,3,4],[3,5,2,4,1],[1,2,3,4,5],[5,4,3,2,1],[1,3,2,4,5],[5,2,1,3,4],[3,5,2,4,1]]
# demands = [0,1,1,1,1,1,1,1,1,1]
# drafts = [9,1,9,9,9,8,9,9,2,9]
costs = []
demands = []
drafts = []
n = 10
seed = 50


def parse_file(fileName):
    with open(fileName, "r") as f:
        num_line = 1
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
        demands = []
        drafts = []

        lines = f.readlines()
        if fileName[:3] == "pcb" or fileName[:4] == 'KroA':
            costs = [[0] * int(n) for i in range(int(n))]
            for line in lines:
                if num_line >= 2 and num_line <= 1 + (int(n)):
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(len(numeros) - 1):
                        costs[num_line-2][i] = (int(numeros[i]))
                if num_line == int(n) + 2:
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(len(numeros) - 2):
                        demands.append(int(numeros[i]))
                if num_line == int(n) + 3:
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(len(numeros) - 1):
                        drafts.append(int(numeros[i]))
                num_line += 1
        else:
            costs = [[0] * int(n) for i in range(int(n))]
            for line in lines:
                if num_line >= 16 and num_line <= 16 + (int(n)-1):
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(int(n)):
                        costs[num_line-16][i] = (int(numeros[i]))
                if num_line == 16 + (int(n)-1) + 9:
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(len(numeros) - 1):
                        demands.append(int(numeros[i]))
                if num_line == 16 + (int(n)-1) + 12:
                    line = line.replace("\n", "")
                    numeros = line.split(" ")
                    for i in range(len(numeros) - 1):
                        drafts.append(int(numeros[i]))
                num_line += 1

        # for line in costs:
         #   print(line)
        # print(demands)
        # print(len(drafts))


def ValidateSolution(x, y):

    global demands
    global costs
    global n
    global drafts

    rest1 = 1
    # Primeiro conjunto de restricoes: soma de todas colunas e igual a 1
    for j in range(0, n):
        rest1 = 0
        for i in range(0, n):
            rest1 += x[i][j]
        if (rest1 != 1):
            print("SOLUCAO NAO E VALIDA: Soma alguma coluna nao e igual a 1")
            return False

    rest2 = 1
    # Segund0 conjunto de restricoes: soma de todas linhas e igual a 1
    for i in range(0, n):
        rest2 = 0
        for j in range(0, n):
            rest2 += x[i][j]
        if (rest2 != 1):
            print("SOLUCAO NAO E VALIDA: Soma de alguma linha nao e igual a 1")
            return False

    rest31 = 0
    rest32 = 0
    # Terceiro conjunto de restricoes: demanda dos portos e atendidas
    for j in range(1, n):
        rest31 = 0
        rest32 = 0
        for i in range(0, n):
            rest31 += y[i][j]
        for i in range(0, n):
            rest32 += y[j][i]
        if ((rest31 - rest32) != demands[j]):
            print("SOLUCAO NAO E VALIDA: Demanda de todos portos nao e atendida")
            return False

    rest41 = 0
    rest42 = 0
    # Quarto conjunto de restricoes: embarcacao sai da garagem carregada com toda demanda necessaria
    for j in range(0, n):
        rest41 += y[0][j]
    for i in range(0, n):
        rest42 += demands[i]

    if rest41 != rest42:
        print("SOLUCAO NAO E VALIDA: Embarcacao nao sai suficientemente carregada (soma das demandas)")
        return False

    rest5 = 0
    # Quinto conjunto de restricoes: so retorna para o porto quando estiver vazio
    for i in range(0, n):
        rest5 += y[i][0]

    if rest5 != 0:
        print("SOLUCAO NAO E VALIDA: Embarcacao retorna para o porto com carga maior que 0")
        return False

    # Sexto conjunto de restricoes: limites de profundidade e implicacao
    for i in range(0, n):
        for j in range(0, n):
            if (y[i][j] < 0 or y[i][j] > drafts[j]*x[i][j]):
                print(
                    "SOLUCAO NAO E VALIDA: Profundidade limite violada ou implicacao de y e x violada")
                return False

    return True


def GenerateInitialPop(initialPop, popSize):
    bestIndividual = GenerateIndividual()
    initialPop.append(bestIndividual)
    best = Evaluate(bestIndividual["x"])
    for i in range(0, popSize - 1):
        currentIndividual = GenerateIndividual()
        initialPop.append(currentIndividual)
        atual = Evaluate(currentIndividual["x"])
        if atual < best:
            best = atual

    return Evaluate(bestIndividual["x"])


def GenerateIndividual():
    global costs
    global demands
    global drafts
    global n
    global seed

    # random.seed(seed)

    solucaoValida = False
    while(not solucaoValida):
        x = [[0] * int(n) for i in range(int(n))]
        y = [[0] * int(n) for i in range(int(n))]
        currentDraft = sum(demands)
        unvisited = list(range(1, n))
        solucao = []
        for i in range(0, n-1):
            validChoices = []
            # print(unvisited)
            for j in range(0, len(unvisited)):
                # print(unvisited[j])
                if drafts[unvisited[j]] >= currentDraft:
                    validChoices.append(unvisited[j])
            chosen = random.choice(validChoices)
            currentDraft = currentDraft - demands[chosen]
            unvisited.remove(chosen)
            solucao.append(chosen)

            x, y = ComputeXY(solucao)
        solucaoValida = ValidateSolution(x, y)

    individual = {
        "x": x,
        "y": y
    }
    return individual


def ComputeXY(solucao):
    global demands
    global n
    x = [[0] * int(n) for i in range(int(n))]
    y = [[0] * int(n) for i in range(int(n))]
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
    return x, y


def EvaluatePop(pop):
    popCosts = []
    for i in range(0, len(pop)):
        individualCost = Evaluate(pop[i]["x"])
        popCosts.append(individualCost)
    return popCosts


def Evaluate(x):
    global costs
    c = costs
    cost = 0
    for i in range(0, n):
        for j in range(0, n):
            cost = cost + x[i][j]*c[i][j]

    return cost

def SelectIndividuals(population, scores, popSize):
    selected = []
    selected.append(population[scores.index(max(scores))])
    maxScore = max(scores)
    while(len(selected) < popSize):
        random_individual = random.randint(0, popSize-1)
        scoreIndividual = scores[random_individual]
        random_number = random.uniform(0, 1)
        if random_number >= (scoreIndividual / maxScore):
            selected.append(population[random_individual])
    return selected

def Reproduce(parentA, parentB):
    valida = False
    global drafts
    while(not valida):
        tourA = RetrieveTour(parentA["x"])
        tourB = RetrieveTour(parentB["x"])

        draftsA = RetrieveDrafts(tourA)
        draftsB = RetrieveDrafts(tourB)

        for i in range(0, len(tourA)):
            for j in range(0, len(tourB)):
                if draftsA[i] == draftsB[j] and tourA[i] != tourB[j]:
                    chance = random.uniform(0, 1)
                    if chance >= 0.5:
                        temp = tourA[i]
                        tourA[tourA.index(tourB[j])] = temp
                        tourA[i] = tourB[j]
                        break

        x, y = ComputeXY(tourA)
        valida = ValidateSolution(x, y)
    
    individual = {
        "x": x,
        "y": y
    }
    return individual

def Mutate(population):
    mutatedPopulation = []
    for individual in population:
        random_number = random.uniform(0, 1)
        if random_number <= 0.2:
            newIndividual = SoftMutation(individual)
            mutatedPopulation.append(newIndividual)
        elif random_number <= 0.25:
            newIndividual = HardMutation(individual)
            mutatedPopulation.append(newIndividual)
        elif random_number <= 0.26:
            newIndividual = GenerateIndividual()
            mutatedPopulation.append(newIndividual)
        elif random_number <= 0.285:
            newIndividual = ScrambleMutation(individual)
            mutatedPopulation.append(newIndividual)
        else:
            mutatedPopulation.append(individual)
    return mutatedPopulation

def SoftMutation(individual):
    tour = RetrieveTour(individual['x'])
    draft = RetrieveDrafts(tour)
    randomDraft = draft[random.randint(0, len(draft) - 1)]
    possibleSwap = []

    for i in range(len(draft)):
        if draft[i] == randomDraft:
            possibleSwap.append(i)

    if len(possibleSwap) >= 2:
        if len(possibleSwap) > 2:
            i, j = random.sample(possibleSwap, 2)
        else:
            i = possibleSwap[0]
            j = possibleSwap[1]

        swappedTour = Swap(tour, i, j)
    else:
        swappedTour = tour

    x, y = ComputeXY(swappedTour)

    newIndividual = {
        "x": x,
        "y": y
    }
    return newIndividual

def HardMutation(individual):
    tour = RetrieveTour(individual['x'])
    draft = RetrieveDrafts(tour)
    randomDraft = draft[random.randint(0, len(draft) - 1)]
    possibleSwap = []
    swappedTour = tour

    for i in range(len(draft)):
        if draft[i] == randomDraft:
            possibleSwap.append(i)

    if len(possibleSwap) > 1:
        for k in range(0, len(possibleSwap)):
            currentTour = swappedTour
            i, j = random.sample(possibleSwap, 2)
            swappedTour = Swap(currentTour, i, j)
    else:
        swappedTour = tour

    x, y = ComputeXY(swappedTour)

    newIndividual = {
        "x": x,
        "y": y
    }

    if (not ValidateSolution(x, y)):
        print("nao valida")
    return newIndividual

def ScrambleMutation(individual):
    newIndividual = []
    global drafts
    draftsIndex = {}
    tour = RetrieveTour(individual['x'])
    draftsLocal = RetrieveDrafts(tour)
    currentTour = []
    swappedTour = tour
    for draft in draftsLocal:
        temp = []
        for i in range(len(tour)):
            if drafts[tour[i]] == draft:
                temp.append(i)
        draftsIndex[str(draft)] = temp

    for key in draftsIndex.keys():
        if len(draftsIndex[key]) > 1:
            for k in range(len(draftsIndex[key])):
                currentTour = swappedTour
                i, j = random.sample(draftsIndex[key], 2)
                swappedTour = Swap(currentTour, i, j)
    #print("Tour original: " + str(tour))
    #print("Tour swappado: " + str(swappedTour))

    x, y = ComputeXY(swappedTour)

    newIndividual = {
        "x": x,
        "y": y
    }

    if (not ValidateSolution(x, y)):
        print("nao valida")
    return newIndividual

def Swap(tour, i, j):
    swappedTour = []
    for k in range(len(tour)):
        if k == i:
            swappedTour.append(tour[j])
        elif k == j:
            swappedTour.append(tour[i])
        else:
            swappedTour.append(tour[k])
    return swappedTour


def RetrieveTour(x):
    tour = []
    line = 0
    while(len(tour) < len(x[0]) - 1):
        for i in range(len(x[line])):
            if x[line][i] == 1:
                tour.append(i)
                line = i
                if len(tour) == len(x[0]):
                    break
    return tour


def RetrieveDrafts(tour):
    global drafts
    tourDrafts = []
    for i in tour:
        tourDrafts.append(drafts[i])
    return tourDrafts


def Reproduction(individuals, popSize):
    newIndividuals = []
    for i in range(0, popSize):
        parentAIndex = random.randint(0, len(individuals)-1)
        parentBIndex = random.randint(0, len(individuals)-1)

        parentA = individuals[parentAIndex]
        parentB = individuals[parentBIndex]

        newIndividual = Reproduce(parentA, parentB)

        newIndividuals.append(newIndividual)

    newIndividuals = Mutate(newIndividuals)

    return newIndividuals


def Evolve(population, scores, popSize):
    newPopulation = []
    topBest = int(popSize * 0.1)
    selectedIndividuals = []
    selectedIndividuals = SelectIndividuals(population, scores, popSize)

    topBestIndex = np.argsort(scores)[:topBest]
    for j in range(0, topBest):
        newPopulation.append(population[topBestIndex[j]])

    newPopulation = newPopulation + (Reproduction(selectedIndividuals, popSize - topBest))

    return newPopulation


def GeneticAlg(initialPop, popSize, iterations):
    newPopulation = initialPop
    scores = []

    for i in range(0, iterations):
        currentPopulation = newPopulation
        scores = EvaluatePop(currentPopulation)
        newPopulation = Evolve(currentPopulation, scores, popSize)
        if len(newPopulation) > popSize:
            print("DEU RUIM")
        #print(scores)

    return currentPopulation[scores.index(min(scores))]


def generate_neighbour(individual):
    pass

def dic_to_file(dic):
    with open("resultados.txt", "w") as f:
        for key in dic.keys():
            line = ""
            for value in dic[key]:
                line += str(value)  + ","
            f.write(line + "\n")


if __name__ == '__main__':
    totalInitialCosts = 0
    totalFinalCosts = 0
    info = {}

    numExecs = 10
    arquivos = ["bayg29_10_1.dat", "bayg29_50_1.dat", "gr17_25_1.dat",  "gr48_10_1.dat",  "gr48_25_1.dat", "ulysses22_50_1.dat"]
    config = [[300, 1600], [300, 1600], [300, 2500] ,[300, 750] ,[300, 750], [300, 2500]]
    bks = [1610, 2743, 2265, 5046, 5161.5, 8290]
    for i in range(len(arquivos)):
        parse_file(arquivos[i])
        initialPop = []

        totalFinalCosts = 0
        totalInitialCosts = 0
        best_results = []
        times = []
        desvio_bks = []
        bestIndividual = {} 
        for j in range(0, numExecs):
            start_time = time.time()
            initialCost = GenerateInitialPop(initialPop, config[i][0])
            totalInitialCosts = totalInitialCosts + initialCost
            bestIndividual = GeneticAlg(initialPop, config[i][0], config[i][1])
            finalCost = Evaluate(bestIndividual["x"])
            best_results.append(finalCost)
            totalFinalCosts = totalFinalCosts + finalCost
            elapsed_time = time.time() - start_time
            times.append(elapsed_time)

            desvio_bks.append(100 * ((finalCost - bks[i])/bks[i]))
        
        bestSolution = RetrieveTour(bestIndividual["x"])
        times_media = sum(times)/ numExecs
        desvio_bks_medio = sum(desvio_bks) / numExecs
        averageFinalCost = totalFinalCosts/numExecs
        averageInitialCost = totalInitialCosts/numExecs
        dp = statistics.stdev(best_results)
        info[str(arquivos[i])] = [averageInitialCost, averageFinalCost, dp, times_media, desvio_bks_medio, bestSolution]
        print("Terminei de rodar " + str(arquivos[i]) + " com tempo = " + str(sum(times)))

        dic_to_file(info)
        
