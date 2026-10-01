import math

def addition(a, b):
    return a + b

def soustraction(a, b): 
    return a - b

def multiplication(a, b):
    return a * b 

def division(a, b):
    return a / b

def puissance(a, b):
    return a ** b 

def modulo(a, b):
    return a % b 

def racine_carre(a):
    return math.sqrt(a) 

def exponentielle(a):
    return math.exp(a)

def racine_carree (nombre):
    if nombre < 0:
        raise ValueError("Le nombre doit être positif ou nul.")
    return math.sqrt(nombre)
