import tkinter as tk
import random

from addition import addition
from multiplication import multiplication
from soustraction import soustraction
from division import division


fenetre = tk.Tk()
fenetre.title("Calculatrice")
fenetre.geometry("500x500")
fenetre.resizable(False, False)


ecran = tk.Entry(
    fenetre,
    font=("Arial", 24),  # correction : font et non front
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
        resultat = addition(
            premier_nombre,
            deuxieme_nombre
        )

    elif operateur == "*":
        resultat = multiplication(
            premier_nombre,
            deuxieme_nombre
        )

    elif operateur == "-":
        resultat = soustraction(
            premier_nombre,
            deuxieme_nombre
        )

    elif operateur == "/":
        try:
            resultat = division(
                premier_nombre,
                deuxieme_nombre
            )

        except ValueError as e:
            ecran.delete(0, tk.END)
            ecran.insert(tk.END, str(e))
            return

    else:
        resultat = "erreur"

    ecran.delete(0, tk.END)
    ecran.insert(tk.END, str(resultat))


# --- ZONE LOGIQUE DU JEU SNAKE ---
canvas_jeu = None
btn_retour = None
btn_recommencer = None
serpent = []
direction = "Right"
pomme = []
score = 0
vitesse = 100
taille_case = 20
jeu_en_cours = False 

def lancer_snake():
    global canvas_jeu, btn_retour, serpent, direction, pomme, score, jeu_en_cours
    
    jeu_en_cours = True
    
    # Masquer l'interface de la calculatrice
    ecran.pack_forget()
    cadre.pack_forget()
    
    # Redimensionnement temporaire pour accueillir le jeu
    fenetre.title("Snake")
    fenetre.geometry("400x460")
    
    # Bouton pour revenir à la calculatrice à tout moment
    btn_retour = tk.Button(fenetre, text="⬅ Retour Calculatrice", font=("Arial", 11), command=quitter_jeu)
    btn_retour.pack(pady=5)
    
    # Zone d'affichage graphique (le Canvas)
    canvas_jeu = tk.Canvas(fenetre, bg="black", width=400, height=400)
    canvas_jeu.pack()
    
    # Positions initiales du serpent (grille de 20x20 pixels)
    serpent = [[100, 100], [80, 100], [60, 100]]
    direction = "Right"
    score = 0
    creer_pomme()
    
    # Raccourcis clavier Linux pour diriger le serpent
    fenetre.bind("<Left>", lambda e: changer_direction("Left"))
    fenetre.bind("<Right>", lambda e: changer_direction("Right"))
    fenetre.bind("<Up>", lambda e: changer_direction("Up"))
    fenetre.bind("<Down>", lambda e: changer_direction("Down"))
    
    boucle_jeu()

def creer_pomme():
    global pomme
    x = random.randint(0, 19) * taille_case
    y = random.randint(0, 19) * taille_case
    pomme = [x, y]

def changer_direction(nouvelle_dir):
    global direction
    opposés = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
    if nouvelle_dir != opposés.get(direction):
        direction = nouvelle_dir

def boucle_jeu():
    global serpent, pomme, score, jeu_en_cours, btn_recommencer
    
    if not jeu_en_cours:
        return 
        
    tête_x, tête_y = serpent[0]
    if direction == "Left": tête_x -= taille_case
    elif direction == "Right": tête_x += taille_case
    elif direction == "Up": tête_y -= taille_case
    elif direction == "Down": tête_y += taille_case
    
    nouvelle_tête = [tête_x, tête_y]
    
    # Vérification des collisions (murs et auto-collision)
    if (tête_x < 0 or tête_x >= 400 or 
        tête_y < 0 or tête_y >= 400 or 
        nouvelle_tête in serpent):
        
        jeu_en_cours = False
        canvas_jeu.create_text(200, 160, text=f"GAME OVER\nScore: {score}", fill="white", font=("Arial", 24), justify="center")
        
        # Bouton Rejouer incrusté directement sur l'écran de fin
        btn_recommencer = tk.Button(fenetre, text="Rejouer 🔄", font=("Arial", 14), bg="#4CAF50", fg="white", command=rejouer)
        canvas_jeu.create_window(200, 240, window=btn_recommencer)
        return

    serpent.insert(0, nouvelle_tête)

    if nouvelle_tête == pomme:
        score += 1
        creer_pomme()
    else:
        serpent.pop()

    canvas_jeu.delete("all")
    canvas_jeu.create_oval(pomme[0], pomme[1], pomme[0]+taille_case, pomme[1]+taille_case, fill="red")
    
    for segment in serpent:
        canvas_jeu.create_rectangle(segment[0], segment[1], segment[0]+taille_case, segment[1]+taille_case, fill="green")
        
    fenetre.after(vitesse, boucle_jeu)

def rejouer():
    global btn_recommencer, canvas_jeu, btn_retour
    if btn_recommencer: btn_recommencer.destroy()
    if canvas_jeu: canvas_jeu.destroy()
    if btn_retour: btn_retour.destroy()
    lancer_snake()

def quitter_jeu():
    global jeu_en_cours, canvas_jeu, btn_retour, btn_recommencer
    
    jeu_en_cours = False
    if canvas_jeu: canvas_jeu.destroy()
    if btn_retour: btn_retour.destroy()
    if btn_recommencer: btn_recommencer.destroy()
    
    # Nettoyage des touches du clavier pour éviter les interférences
    fenetre.unbind("<Left>")
    fenetre.unbind("<Right>")
    fenetre.unbind("<Up>")
    fenetre.unbind("<Down>")
    
    # Rétablissement de l'affichage initial de la calculatrice
    fenetre.title("Calculatrice")
    fenetre.geometry("500x500")
    ecran.pack(padx=10, pady=20, fill="x")
    cadre.pack()
# -------------------------------------


cadre = tk.Frame(fenetre)
cadre.pack()


boutons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
    ("C", 5, 0), ("🐍", 5, 1) # Ajout de la touche secrète Snake à côté du C
]


for texte, ligne, colonne in boutons:

    # Ajustement global : largeur passée de 5 à 6 pour éviter les boutons tronqués
    if texte == "=":

        bouton = tk.Button(
            cadre,
            text=texte,
            font=("Arial", 18),
            width=6,
            height=2,
            command=calculer
        )

    elif texte == "C":

        bouton = tk.Button(
            cadre,
            text=texte,
            font=("Arial", 18),
            width=6,
            height=2,
            command=effacer
        )

    elif texte == "🐍":

        bouton = tk.Button(
            cadre,
            text=texte,
            font=("Arial", 18),
            width=6,
            height=2,
            command=lancer_snake
        )

    elif texte in "+-*/":

        bouton = tk.Button(
            cadre,
            text=texte,
            font=("Arial", 18),
            width=6,
            height=2,
            command=lambda op=texte: choisir_operateur(op)
        )

    else:

        bouton = tk.Button(
            cadre,
            text=texte,
            font=("Arial", 18),
            width=6,
            height=2,
            command=lambda n=texte: ajouter(n)
        )

    bouton.grid(
        row=ligne,
        column=colonne,
        padx=3,
        pady=3
    )


fenetre.mainloop()


