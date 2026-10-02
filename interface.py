import tkinter as tk
import random

# Conserve tes imports "addition, multiplication..." ici s'ils sont dans ton dossier
try:
    from addition import addition
    from multiplication import multiplication
    from soustraction import soustraction
    from division import division
except ImportError:
    addition = lambda a, b: a + b
    multiplication = lambda a, b: a * b
    soustraction = lambda a, b: a - b
    division = lambda a, b: a / b if b != 0 else "erreur"

fenetre = tk.Tk()
fenetre.title("Calculatrice")
fenetre.geometry("500x500")
fenetre.resizable(False, False)

ecran = tk.Entry(fenetre, font=("Arial", 24), justify="right")
ecran.pack(padx=10, pady=20, fill="x")

premier_nombre = None
operateur = None

def ajouter(nombre): ecran.insert(tk.END, str(nombre))
def effacer(): ecran.delete(0, tk.END)

def choisir_operateur(op):
    global premier_nombre, operateur
    premier_nombre = float(ecran.get())
    operateur = op
    effacer()

def calculer():
    global premier_nombre, operateur
    deuxieme_nombre = float(ecran.get())

    if operateur == "+": resultat = addition(premier_nombre, deuxieme_nombre)
    elif operateur == "*": resultat = multiplication(premier_nombre, deuxieme_nombre)
    elif operateur == "-": resultat = soustraction(premier_nombre, deuxieme_nombre)
    elif operateur == "/":
        try: resultat = division(premier_nombre, deuxieme_nombre)
        except ValueError as e:
            ecran.delete(0, tk.END)
            ecran.insert(tk.END, str(e))
            return
    else: resultat = "erreur"

    ecran.delete(0, tk.END)
    ecran.insert(tk.END, str(resultat))


# --- ZONE LOGIQUE DU SNAKE GRAPHISME 100% CODE ---
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
    
    ecran.pack_forget()
    cadre.pack_forget()
    
    fenetre.title("Snake Retro HD")
    fenetre.geometry("400x460")
    
    btn_retour = tk.Button(fenetre, text="⬅ Retour Calculatrice", font=("Arial", 11), command=quitter_jeu)
    btn_retour.pack(pady=5)
    
    # highlightthickness=0 enlève la bordure blanche autour du Canvas
    canvas_jeu = tk.Canvas(fenetre, width=400, height=400, highlightthickness=0)
    canvas_jeu.pack()
    
    serpent = [[100, 100], [80, 100], [60, 100]]
    direction = "Right"
    score = 0
    creer_pomme()
    
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

def dessiner_decor():
    """Génère dynamiquement la pelouse à damier bicolore (style Google Snake)"""
    for ligne in range(20):
        for col in range(20):
            x1 = col * taille_case
            y1 = ligne * taille_case
            x2 = x1 + taille_case
            y2 = y1 + taille_case
            
            # Si la somme de la ligne et de la colonne est paire -> vert clair, sinon vert foncé
            if (ligne + col) % 2 == 0:
                couleur = "#AAD751"  # Vert clair Google
            else:
                couleur = "#A2D149"  # Vert foncé Google
                
            canvas_jeu.create_rectangle(x1, y1, x2, y2, fill=couleur, outline="")

def dessiner_yeux(x, y):
    """Calcule et dessine les yeux du serpent pour qu'ils regardent dans la bonne direction"""
    # Coordonnées par défaut des deux yeux par rapport au carré de la tête
    if direction == "Right":
        oeil1_box = (x+12, y+3, x+17, y+8)
        oeil2_box = (x+12, y+12, x+17, y+17)
        pup1_box = (x+15, y+5, x+17, y+7)
        pup2_box = (x+15, y+14, x+17, y+16)
    elif direction == "Left":
        oeil1_box = (x+3, y+3, x+8, y+8)
        oeil2_box = (x+3, y+12, x+8, y+17)
        pup1_box = (x+3, y+5, x+5, y+7)
        pup2_box = (x+3, y+14, x+5, y+16)
    elif direction == "Up":
        oeil1_box = (x+3, y+3, x+8, y+8)
        oeil2_box = (x+12, y+3, x+17, y+8)
        pup1_box = (x+5, y+3, x+7, y+5)
        pup2_box = (x+14, y+3, x+16, y+5)
    else: # Down
        oeil1_box = (x+3, y+12, x+8, y+17)
        oeil2_box = (x+12, y+12, x+17, y+17)
        pup1_box = (x+5, y+15, x+7, y+17)
        pup2_box = (x+14, y+15, x+16, y+17)

    # Dessin du blanc des yeux
    canvas_jeu.create_oval(oeil1_box, fill="white", outline="")
    canvas_jeu.create_oval(oeil2_box, fill="white", outline="")
    # Dessin des pupilles noires
    canvas_jeu.create_oval(pup1_box, fill="black", outline="")
    canvas_jeu.create_oval(pup2_box, fill="black", outline="")

def boucle_jeu():
    global serpent, pomme, score, jeu_en_cours, btn_recommencer
    if not jeu_en_cours: return 
        
    tête_x, tête_y = serpent[0]
    if direction == "Left": tête_x -= taille_case
    elif direction == "Right": tête_x += taille_case
    elif direction == "Up": tête_y -= taille_case
    elif direction == "Down": tête_y += taille_case
    
    nouvelle_tête = [tête_x, tête_y]
    
    if (tête_x < 0 or tête_x >= 400 or tête_y < 0 or tête_y >= 400 or nouvelle_tête in serpent):
        jeu_en_cours = False
        canvas_jeu.create_text(200, 160, text=f"GAME OVER\nScore: {score}", fill="white", font=("Arial", 24), justify="center")
        btn_recommencer = tk.Button(fenetre, text="Rejouer 🔄", font=("Arial", 14), bg="#4CAF50", fg="white", command=rejouer)
        canvas_jeu.create_window(200, 240, window=btn_recommencer)
        return

    serpent.insert(0, nouvelle_tête)

    if nouvelle_tête == pomme:
        score += 1
        creer_pomme()
    else:
        serpent.pop()

    # On nettoie tout
    canvas_jeu.delete("all")
    
    # 1. Rendu du Décor Quadrillé Dynamique
    dessiner_decor()
        
    # 2. Rendu de la Pomme Stylisée (Corps rouge + petite feuille verte)
    px, py = pomme[0], pomme[1]
    canvas_jeu.create_oval(px, py, px+taille_case, py+taille_case, fill="#E63946", outline="") # Pomme
    canvas_jeu.create_rectangle(px+8, py-3, px+12, py+2, fill="#4C9130", outline="") # Petite queue/feuille
    
    # 3. Rendu du Serpent Stylisé
    for index, segment in enumerate(serpent):
        sx, sy = segment[0], segment[1]
        if index == 0:
            # TÊTE : Un cercle un poil plus gros aux bords arrondis
            canvas_jeu.create_oval(sx, sy, sx+taille_case, sy+taille_case, fill="#4E7AA6", outline="") # Tête bleue/verte design
            dessiner_yeux(sx, sy)
        else:
            # CORPS : Des ronds parfaits qui se suivent au lieu de vieux cubes rectangles
            canvas_jeu.create_oval(sx+1, sy+1, sx+taille_case-1, sy+taille_case-1, fill="#5B8AD9", outline="")
        
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
    
    fenetre.unbind("<Left>")
    fenetre.unbind("<Right>")
    fenetre.unbind("<Up>")
    fenetre.unbind("<Down>")
    
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
    ("C", 5, 0), ("🐍", 5, 1)
]

for texte, ligne, colonne in boutons:
    if texte == "=": bouton = tk.Button(cadre, text=texte, font=("Arial", 18), width=6, height=2, command=calculer)
    elif texte == "C": bouton = tk.Button(cadre, text=texte, font=("Arial", 18), width=6, height=2, command=effacer)
    elif texte == "🐍": bouton = tk.Button(cadre, text=texte, font=("Arial", 18), width=6, height=2, command=lancer_snake)
    elif texte in "+-*/": bouton = tk.Button(cadre, text=texte, font=("Arial", 18), width=6, height=2, command=lambda op=texte: choisir_operateur(op))
    else: bouton = tk.Button(cadre, text=texte, font=("Arial", 18), width=6, height=2, command=lambda n=texte: ajouter(n))
    bouton.grid(row=ligne, column=colonne, padx=3, pady=3)

fenetre.mainloop()



