import random


def mutation(list_gen:list):
    for i in list_gen:
        if round(random.random()):
            i = not(i)


class Person:
    def __init__(self):
        self.gen = []


person = Person()
        
