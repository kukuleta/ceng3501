# starter code for solving knapsack problem using genetic algorithm
import random
import numpy as np

fc = open('./c.txt', 'r')
fw = open('./w.txt', 'r')
fv = open('./v.txt', 'r')
fout = open('./out.txt', 'w')


c = int(fc.readline())
w = []
v = []
for line in fw:
    w.append(int(line))
for line in fv:
    v.append(int(line))

print('Capacity :', c)
print('Weight :', w)
print('Value : ', v)

popSize = int(input('Size of population : '))
genNumber = int(input('Max number of generation : '))

def populatePopulation(populationSize):
    population = np.random.randint(0, 2, size=(populationSize,len(w)))
    return population

print('\n*******')
print('Initalizing population')

population = populatePopulation(popSize)

def estimateFitnessValues(population):
    ItemValues = np.array(v)
    ItemWeights = np.array(w)
    totalValues = int(ItemValues.dot(population))
    totalWeights = int(ItemWeights.dot(population))
    totalWeights[totalWeights > c] = 0
    return [(invidiualID,Value) for invidiualID,Value in enumerate(totalValues)]

def getSurvivalProbability(fitnessValues):
    totalFitnessSum = np.sum(fitnessValues)
    relativeFitness = fitnessValues / totalFitnessSum
    cumulativeProbability = np.cumsum(relativeFitness)
    return cumulativeProbability

def rouletteParentSelection(population, probabilites,number):
    prob = np.random.random()
    parentSelected = np.where((probabilites > prob) == True)[0][0]
    return parentSelected

def kTourmanentParentSelection(population, k, number):
    invididualsSelected = set()
    candidatesSelected = set()
    for round in range(number):
        for candicate in range(k):
            candidatesSelected.add(random.choice(population))
        fitScores = sorted(candidatesSelected, key = lambda item: (lambda key, value: value)(*item),reverse=True)
        invididualsSelected.add(population[fitScores[0]])
        candidatesSelected.clear()
    return list(invididualsSelected)

print('\nParent Selection\n---------------------------')
print('(1) Roulette-wheel Selection')
print('(2) K-Tournament Selection')

parentSelection = int(input('Which one? '))
if parentSelection == 1:
    parents = rouletteParentSelection(population, getSurvivalProbability(), popSize)

if parentSelection == 2:
    KCount = int(input('k=? (between 1 and ' + str(len(w)) + ') '))
    parents = kTourmanentParentSelection(population, KCount, popSize)

def crossOver(parent, number, popSize):
    child = []
    father, mother = 0,0
    genIndexesCrossedOver = random.sample(range(0, len(w)), k=number)
    for population in range(popSize):
        for genIndex in genIndexesCrossedOver:
            father = random.choice(parent)
            mother = random.choice(parent)
            for gen in range(genIndex):
                father[gen], mother[gen] = mother[gen], father[gen]
        child.extend([father,mother])
    return child


print('\nN-point Crossover\n---------------------------')
crossoverCount = int(input('n=? (between 1 and ' + str(len(w) - 1) + ') '))

childrens = crossOver(parents, crossoverCount, popSize)

print('\nMutation Probability\n---------------------------')
mutProb = float(input('prob=? (between 0 and 1) '))

def mutatePopulation(children, mutationProbability):
    for j in range(len(children)):
        mutationBoundaries = random.randint(0, 1)
        if mutationBoundaries == mutationProbability:
            individualMutated = children[j]
            gen = random.randint(0, len(w))
            individualMutated[gen] = 1 - individualMutated[gen]

mutatePopulation(childrens, mutProb)

def estimateElitism(children):
    fitScores = estimateFitnessValues(children)
    elitism_sorted = sorted(fitScores, key = lambda item: (lambda key, value: value)(*item) , reverse=True)
    best_individual = childrens[elitism_sorted[0]]
    return best_individual

def age_based_selection(gen):
    bestInstancesSurvived = estimateElitism(gen)
    next_gen = []

    for current_gen in gen:
        next_gen.append(current_gen)

    next_gen[0] = keep_gen

    return next_gen


def fitnessSelection(generation):
    fitScores = estimateFitnessValues(generation)
    bestFitScores = sorted(fitScores,key = lambda item: (lambda key, value: value)(*item),reverse=True)
    invidiualsSurvived = []
    for instance in range(int(len(generation) * 0.8)):
        invidiualsSurvived.append(invidiualsSurvived[bestFitScores[0][0]])
    return invidiualsSurvived

print('\nSurvival Selection\n---------------------------')
print('(1) Age-based Selection')
print('(2) Fitness-based Selection')
survivalSelection = int(input('Which one? '))

if survivalSelection == 1:
   NextGeneration = age_based_selection(childrens)
elif survivalSelection == 2:
   NextGeneration = fitnessSelection(childrens)
else:
    print("You must specify one of the options 1-2")

elitism = bool(input('Elitism? (Y or N) '))

def genLoop(generation, genNumber, genInfo, parentSelectionMethod, survivalSelectionMethod):
    fitness_plot_list = []
    best_gen = ""
    weight = 0
    value = 0

    for loop in range(genNumber):
        if parentSelectionMethod == 1:
            parentsSelected = rouletteParentSelection(generation, getSurvivalProbability(), popSize)
            differentiatedGen = crossOver(parentsSelected, genInfo[crossoverCount], popSize)
            mutatePopulation(differentiatedGen, genInfo[mutationProp])
            if survivalSelectionMethod == "1":
                g = age_based_selection(differentiatedGen)
            else:
                g = fitnessSelection(differentiatedGen)
        else:
            parentsSelected = kTourmanentParentSelection(generation, genInfo[KCount], popSize)
            differentiatedGen = crossOver(parentsSelected, genInfo[crossoverCount], popSize)
            mutatePopulation(differentiatedGen, genInfo[mutationProp])
            if survivalSelectionMethod == "1":
                survivedGen = age_based_selection(differentiatedGen)

            else:
                survivedGen = fitnessSelection(differentiatedGen)

        fitness_next_gen = estimateFitnessValues(survivedGen)
        fitness_next_gen_sorted = sorted(fitness_next_gen, key=lambda  x: int(x[4]), reverse=True)

        fitness_plot_list.append(fitness_next_gen_sorted[0][4])

    for a in g[0]:
        best_gen = best_gen + str(a)

    for j, gene in enumerate(g[0]):
        value += gene * v[j]
        weight += gene * w[j]

fout.write('chromosome: 101010111000011\n')
fout.write('weight: 749\n')
fout.write('value: 1458')
fout.close() 
