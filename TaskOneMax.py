# Имя: Турнирный отбор
# Скрещивание: Одноточечное скрещивание
# Мутация: Инвертирование бита
#

# импорты бибилиотек
from random import *

# # <------------------- создадим константы для общей работы ------------------->
LEN_CHROMOSOME = 8  # длина каждой "хромосомы"

COUNT_PERSON = 20  # количесвто индивидов в популяции
PROBABILITY_CROSSING = 0.9  # шанс скрещивания ( по идее можно взять и 1(100%))
PROBABILITY_MUTATION = 0.1  # шанс мутации

COUNT_GENERATION = 200  # количество поколений ( итераций)


# <------------------- Описание генетического алгоритма ------------------->

# класс для взаимодействия с преспособленностью
class CalculatorFitness():
    def __init__(self):
        self.values = [0]


# класс индивида, наследующий list
class Individ(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.fitness = CalculatorFitness()


# вычисление преспособленности индивида, функция вернет кортеж из суммы
def calculator_fitness_individ(instance_individ):
    return sum(instance_individ),


# функция по созданию характеристик для индивида
# соответсвенно создаем индивида
def create_individ():
    return Individ([randint(0, 1) for _ in range(LEN_CHROMOSOME)])


# создание популяции из индивидумов, функция вернет список индивидумов
def create_population(size=COUNT_GENERATION):
    return list([create_individ() for _ in range(size)])


# функция для создания клона индивида
# это нужно для того, чтобы при случайном выборе вышел один и тот же результат
# можно было сохранить самого индивида и его клона
def clone_individ(value):
    clone = Individ(value[:])
    clone.fitness.values[0] = value.fitness.values[0]
    return clone


# функция турнирного отбора
# вернет список особей с максимальной приспособленностью
def tournament_selection(instance_population, size_population):
    list_selection_individ = []
    for i in range(size_population):
        ind1 = ind2 = ind3 = 0
        while ind1 == ind2 or ind2 == ind3 or ind1 == ind3:
            ind1 = randint(0, size_population - 1)
            ind2 = randint(0, size_population - 1)
            ind3 = randint(0, size_population - 1)

        list_selection_individ.append(max(
            [instance_population[ind1],
             instance_population[ind2],
             instance_population[ind3]],
            key=lambda ind: ind.fitness.values[0]))
    return list_selection_individ


# функция скрещивания для образования новых индивидов
# разрез хромосомы задается случайны образом
def crossing_individs(parent1, parent2):
    cut_point_chromosome = randint(2, len(parent1) - 3)
    parent1[cut_point_chromosome:], parent2[cut_point_chromosome:] = parent2[cut_point_chromosome:], parent1[
                                                                                                    cut_point_chromosome:]


# функция мутации
# мутация происходит с неким шансом
# при правином условии меняем отдлеьный ген на противоположный
def mutation(instance_individ, chance_mutation_one_gen=0.01):
    for indexs in range(len(instance_individ)):
        if random() < chance_mutation_one_gen:
            instance_individ[indexs] = int(not (instance_individ[indexs]))


# <------------------- Начало работы ------------------->

population = create_population(size=COUNT_PERSON)
CountGeneration = 0

value_fitness = list(map(calculator_fitness_individ, population))

for individual, value_fitness in zip(population, value_fitness):
    individual.fitness.values = value_fitness

maxFitnessValue = []
averageFitnessValue = []

value_fitness = [individual.fitness.values[0] for individual in population]

while max(value_fitness) < LEN_CHROMOSOME or CountGeneration < COUNT_GENERATION:
    CountGeneration += 1
    best_instance = tournament_selection(population, len(population))
    best_instance = list(map(clone_individ, best_instance))

    for child1, child2 in zip(best_instance[::2], best_instance[1::2]):
        if random() < PROBABILITY_CROSSING:
            crossing_individs(child1, child2)

    for mutant in best_instance:
        if random() < PROBABILITY_CROSSING:
            mutation(mutant, chance_mutation_one_gen=1 / LEN_CHROMOSOME)

    freshFitnessValue = list(map(calculator_fitness_individ, best_instance))
    for individual, value_fitness in zip(best_instance, freshFitnessValue):
        individual.fitness.values = value_fitness

    population[:] = best_instance

    value_fitness = [ind.fitness.values[0] for ind in population]

    maxFitness = max(value_fitness)
    averageFitness = sum(value_fitness) / len(population)

    maxFitnessValue.append(maxFitness)
    averageFitnessValue.append(averageFitness)

    print(
        f"Поколение {CountGeneration}: Максимальная приспособленность = {maxFitness}, средняя = {averageFitnessValue}")

    index_best_individual = value_fitness.index(max(value_fitness))
    print(f"Лучший: №{index_best_individual+1} =", *population[index_best_individual])
    print("\n"*3)