from addition import addition
from multiplication import multiplication
from soustraction import soustraction
from division import division

def afficher_menu():
    print("=== Calculatrice ===")
    print("1. Addition")
    print("2. Multiplication")
    print("3. Soustraction")
    print("4. Division")
    print("5. Quitter")

def demander_nombre(message):
    while True:
        try:
            return float(input(message))
        except ValueError:
            print("Veuillez entrer un nombre valide.")

def lancer_calculatrice():
    while True:
        afficher_menu()
        choix = input("Choisissez une option (1-5): ")

        if choix == '5':
            print("Au revoir !")
            break

        a = demander_nombre("Entrez le premier nombre: ")
        b = demander_nombre("Entrez le deuxième nombre: ")
        
        if choix == '1':
            resultat = addition(a, b)
            print(f"Résultat de l'addition: {resultat}")
            
        elif choix == '2':
            resultat = multiplication(a, b)
            print(f"Résultat de la multiplication: {resultat}")
            
        elif choix == '3':
            resultat = soustraction(a, b)
            print(f"Résultat de la soustraction: {resultat}")
            
        elif choix == '4':
            try:
                resultat = division(a, b)
                print(f"Résultat de la division: {resultat}")
            except ValueError as e:
                print(e)
        else:
            print("Option invalide. Veuillez réessayer.")
if __name__ == "__main__":
    lancer_calculatrice()
