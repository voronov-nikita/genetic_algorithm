# Задача по нахождению минимального маршрута
# Для решения данной задачи требуется базовая модель создания генетического алгоритма
# Для постороения индивидов используется библиотека deap
# Поиск минимального саршрута осуществляется через индексацию кортежей (или списков)
#

# pip install deap
from deap import base, algorithms, creator, tools

from random import *
import matplotlib.pyplot as plt
import numpy as np

# <------------------- создадим константы для общей работы ------------------->
inf = 100
# здесь указывается все возможные пути
# количество элементов в каждом 1-м кортеже - количесвто точек
# количество элементов в кортеже кортежа - все возможные пути,
# если путя не существует, на его место встает бесконечное число
# другими словами используется матрица смежности
matrix_sm = (
    (0, 3, 1, 3, inf, inf),
    (3, 0, 4, inf, inf, inf),
    (1, 4, 0, inf, 7, 5),
    (3, inf, inf, 0, inf, 2),
    (inf, inf, 7, inf, 0, 4),
    (inf, inf, 5, 2, 4, 0),
)
# откуда начинается старт
starting_poin = 0
LEN_VARIOUS = len(matrix_sm)
# длина хромосомы (
LEN_CHROMOSOME = len(matrix_sm) * len(matrix_sm[0])

COUNT_PERSON = 500  # количесвто индивидов в популяции
PROBABILITY_CROSSING = 0.99  # шанс скрещивания ( по идее можно взять и 1(100%))
PROBABILITY_MUTATION = 0.1  # шанс мутации

COUNT_GENERATION = 30  # количество поколений ( итераций)


# <------------------- Описание генетического алгоритма ------------------->

creator.create("MinFitness", base.Fitness, weights=(-1.0,))
creator.create("Individ", list, fitness=creator.MinFitness)

toolbox = base.Toolbox()
toolbox.register("randomOrder", sample, range(LEN_VARIOUS), LEN_VARIOUS)
toolbox.register("individCreate", tools.initRepeat, creator.Individ, toolbox.randomOrder, LEN_VARIOUS)
toolbox.register("populationCreate", tools.initRepeat, list, toolbox.individCreate)


# <------------------- функции обработки информации ------------------->
# функция вычисления приспособлености индивида
# вернет кортеж из одного числа
def calculator_fitness(individual):
    s = 0
    for n, path in enumerate(individual):
        path = path[:path.index(n) + 1]
        si = starting_poin
        for i in path:
            s += matrix_sm[si][i]
            si = i
    return s,


# функция определения скрещивания
def type_crossing(ind1, ind2):
    for p1, p2 in zip(ind1, ind2):
        # это встроенно в tools
        tools.cxOrdered(p1, p2)
    return ind1, ind2


# функция вычисленич порядка мутации
def order_mutation(individual, indpb):
    for indexind in individual:
        tools.mutShuffleIndexes(indexind, indpb)

    return individual,


toolbox.register("evaluate", calculator_fitness)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("mate", type_crossing)
toolbox.register("mutate", order_mutation, indpb=1.0 / LEN_CHROMOSOME / 10)

# <------------------- Решение алгоритма ------------------->

population = toolbox.populationCreate(n=COUNT_PERSON)

stat = tools.Statistics(lambda indexing: indexing.fitness.values)
stat.register("MinValue", np.min)
stat.register("averageValue", np.mean)

population, logbook = algorithms.eaSimple(
    population, toolbox,
    cxpb=PROBABILITY_CROSSING / LEN_VARIOUS,
    mutpb=PROBABILITY_MUTATION / LEN_VARIOUS,
    ngen=COUNT_GENERATION,
    stats=stat,
    verbose=True
)

MaxFitnessValue, MeanFitnessValue = logbook.select("MinValue", "averageValue")

# <------------------- Графическое отображение ------------------->

plt.plot(MaxFitnessValue, color="red")
plt.plot(MeanFitnessValue, color="blue")
plt.xlabel("Поколение")
plt.ylabel("Приспособленость")


plt.show()

