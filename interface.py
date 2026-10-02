import tkinter as tk

from addition import addition
from multiplication import multiplication
from soustraction import soustraction
from division import division


fenetre = tk.Tk()
fenetre.title("Calculatrice")
fenetre.geometry("350x500")
fenetre.resizable(False, False)


# Écran
ecran = tk.Entry(
    fenetre,
    font=("Arial", 24),
    justify="right"
)

ecran.pack(
    padx=10,
    pady=20,
    fill="x"
)


premier_nombre = None
operateur = None


def ajouter(nombre):
    ecran.insert(tk.END, str(nombre))


def effacer():
    ecran.delete(0, tk.END)


def choisir_operateur(op):
    global premier_nombre
    global operateur

    premier_nombre = float(ecran.get())
    operateur = op
    effacer()


def calculer():
    global premier_nombre
    global operateur

    deuxieme_nombre = float(ecran.get())

    if operateur == "+":
        resultat = addition(premier_nombre, deuxieme_nombre)

    elif operateur == "*":
        resultat = multiplication(premier_nombre, deuxieme_nombre)

    elif operateur == "-":
        resultat = soustraction(premier_nombre, deuxieme_nombre)

    elif operateur == "/":
        try:
            resultat = division(premier_nombre, deuxieme_nombre)

        except ValueError as e:
            ecran.delete(0, tk.END)
            ecran.insert(tk.END, str(e))
            return

    else:
        resultat = "erreur"

    ecran.delete(0, tk.END)
    ecran.insert(tk.END, str(resultat))


# Cadre des boutons
cadre = tk.Frame(fenetre)
cadre.pack(
    padx=10,
    fill="both",
    expand=True
)


boutons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
    ("C", 5, 0)
]


# Permet aux colonnes de s'adapter à la largeur
for colonne in range(4):
    cadre.columnconfigure(colonne, weight=1)


for texte, ligne, colonne in boutons:

    if texte == "=":
        bouton = tk.Button(
            cadre,
            text=texte,
            font=("Arial", 18),
            width=3,
            height=2,
            command=calculer
        )

    elif texte == "C":
        bouton = tk.Button(
            cadre,
            text=texte,
            font=("Arial", 18),
            width=3,
            height=2,
            command=effacer
        )

    elif texte in "+-*/":
        bouton = tk.Button(
            cadre,
            text=texte,
            font=("Arial", 18),
            width=3,
            height=2,
            command=lambda op=texte: choisir_operateur(op)
        )

    else:
        bouton = tk.Button(
            cadre,
            text=texte,
            font=("Arial", 18),
            width=3,
            height=2,
            command=lambda n=texte: ajouter(n)
        )

    bouton.grid(
        row=ligne,
        column=colonne,
        padx=3,
        pady=3,
        sticky="nsew"
    )


fenetre.mainloop()
