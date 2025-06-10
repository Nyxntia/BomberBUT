import tkinter as tk
from tkinter import PhotoImage
from modele import (
    trouver_joueur, bouger_joueur, poser_bombe, diminuer_timers,
    faire_exploser, apparition_fantomes as logique_apparition_fantomes,
    deplacer_fantomes )
from constantes import *

etat_jeu = {
    "carte": None,
    "joueur_x": None,
    "joueur_y": None,
    "fantomes": [],
    "bombes": [],
    "score": 0,
    "timer_global": TIMER_GLOBAL,
    "timer_fantome": TIMER_FANTOME,
    "pv": PV_INITIAL,
    "jeu_actif": True,
    "fenetre": None
}

# Chemins des images
MUR_CASSABLE_IMG = "graphique/img/cassable.png"
MUR_INCASSABLE_IMG = "graphique/img/incassable.png"
FANTOME_IMG = "graphique/img/fantome.png"
JOUEUR_IMG = "graphique/img/bomberman.png"
BOMBE_IMG = "graphique/img/bombe.png"
HERBE_IMG = "graphique/img/herbe.png"  # Image pour les cases vides

def initialiser_jeu(fenetre, carte_initiale, timer_global, timer_fantome):
    """Initialise l'interface graphique et l'état du jeu."""
    # Mise à jour des variables globales
    etat_jeu["carte"] = [list(ligne) for ligne in carte_initiale]
    etat_jeu["joueur_x"], etat_jeu["joueur_y"] = trouver_joueur(etat_jeu["carte"])
    etat_jeu["fantomes"] = []
    etat_jeu["bombes"] = []
    etat_jeu["score"] = 0
    etat_jeu["timer_global"] = TIMER_GLOBAL
    etat_jeu["timer_fantome"] = TIMER_FANTOME
    etat_jeu["jeu_actif"] = True
    etat_jeu["fenetre"] = fenetre

    # Chargement des images
    img_mur_cassable = PhotoImage(file=MUR_CASSABLE_IMG)
    img_mur_incassable = PhotoImage(file=MUR_INCASSABLE_IMG)
    img_fantome = PhotoImage(file=FANTOME_IMG)
    img_joueur = PhotoImage(file=JOUEUR_IMG)
    img_bombe = PhotoImage(file=BOMBE_IMG)
    img_herbe = PhotoImage(file=HERBE_IMG)

    # Création du canvas et des labels
    canvas = tk.Canvas(fenetre, width=len(etat_jeu["carte"][0]) * TAILLE_CASE,
                       height=len(etat_jeu["carte"]) * TAILLE_CASE)
    canvas.pack()
    label_score = tk.Label(fenetre, text=f"Score : {etat_jeu['score']} | PV : {etat_jeu['pv']}", font=("Arial", 14))
    label_score.pack()
    label_timer = tk.Label(fenetre, text=f"Temps restant : {etat_jeu['timer_global']}s", font=("Arial", 14))
    label_timer.pack()

    def dessiner_carte():
        """Affiche la carte sur le canvas."""
        if not etat_jeu["jeu_actif"]:
            return                      # Ne fait rien si le jeu est terminé
        canvas.delete("all")            # Efface tout ce qui est affiché
        for y, ligne in enumerate(etat_jeu["carte"]):
            for x, case in enumerate(ligne):
                if case == "M":
                    canvas.create_image(x * TAILLE_CASE, y * TAILLE_CASE, anchor=tk.NW, image=img_mur_cassable)
                elif case == "C":
                    canvas.create_image(x * TAILLE_CASE, y * TAILLE_CASE, anchor=tk.NW, image=img_mur_incassable)
                elif case == "F":
                    canvas.create_image(x * TAILLE_CASE, y * TAILLE_CASE, anchor=tk.NW, image=img_fantome)
                elif case == "P":
                    canvas.create_image(x * TAILLE_CASE, y * TAILLE_CASE, anchor=tk.NW, image=img_joueur)
                elif case == "B":
                    canvas.create_image(x * TAILLE_CASE, y * TAILLE_CASE, anchor=tk.NW, image=img_bombe)
                else:  # Case vide (herbe)
                    canvas.create_image(x * TAILLE_CASE, y * TAILLE_CASE, anchor=tk.NW, image=img_herbe)

        label_score.config(text=f"Score : {etat_jeu['score']} | PV : {etat_jeu['pv']}")   # Mise à jour de l'affichage du score

    def decrementer_timer():
        """Diminue le timer global et met à jour l'interface."""
        if not etat_jeu["jeu_actif"]:
            return

        etat_jeu["timer_global"] -= 1
        label_timer.config(text=f"Temps restant : {etat_jeu['timer_global']}s")   # Mise à jour de l'affichage du timer

        if etat_jeu["timer_global"] == 0:
            print("Temps écoulé ! Fin du jeu !")
            print(f"Score final : {etat_jeu['score']}")
            etat_jeu["jeu_actif"] = False
            fenetre.destroy()
        else:
            fenetre.after(1000, decrementer_timer)

    def gestion_bombes():
        """Gère les bombes et leurs explosions."""
        if not etat_jeu["jeu_actif"]:
            return

        etat_jeu["bombes"] = diminuer_timers(etat_jeu["bombes"])   # Réduit les timers des bombes
        a_exploser = [(x, y) for x, y, timer in etat_jeu["bombes"] if timer == 1]  # Liste des bombes qui doivent exploser

        for x, y in a_exploser:     # Déclenchement de l'explosion
            etat_jeu["score"] = faire_exploser(
                etat_jeu["carte"],
                x,
                y,
                etat_jeu["score"],
                portee=2,
                joueur_pos=(etat_jeu["joueur_x"], etat_jeu["joueur_y"]),
                etat_jeu=etat_jeu,
            )

        dessiner_carte()     # Redessiner carte après explosion
        if etat_jeu["jeu_actif"]:
            fenetre.after(500, gestion_bombes)

    def gerer_apparition_fantomes():
        """Ajoute des fantômes."""
        if not etat_jeu["jeu_actif"]:
            return

        nouveaux_fantomes = logique_apparition_fantomes(etat_jeu["carte"])
        etat_jeu["fantomes"].extend(nouveaux_fantomes)
        dessiner_carte()

        if etat_jeu["jeu_actif"]:
            fenetre.after(20000, gerer_apparition_fantomes)

    def gestion_fantomes():
        """Gère le déplacement des fantômes."""
        if not etat_jeu["jeu_actif"]:
            return

        etat_jeu["fantomes"] = deplacer_fantomes(
            etat_jeu["carte"],
            etat_jeu["fantomes"],
            etat_jeu["joueur_x"],
            etat_jeu["joueur_y"],
            etat_jeu,
        )
        dessiner_carte()

        if etat_jeu["jeu_actif"]:
            fenetre.after(1000, gestion_fantomes)

    def deplacer_joueur(event):
        """Déplace le joueur."""
        directions = {"Up": "haut", "Down": "bas", "Left": "gauche", "Right": "droite"}
        direction = directions.get(event.keysym)

        if direction:
            nx, ny = bouger_joueur(etat_jeu["carte"], etat_jeu["joueur_x"],  # Déplace le joueur dans la direction donnée
                                   etat_jeu["joueur_y"],
                                   direction)
            if (nx, ny) != (etat_jeu["joueur_x"], etat_jeu["joueur_y"]):
                dessiner_carte()
                etat_jeu["joueur_x"], etat_jeu["joueur_y"] = nx, ny           # Redessine la carte après le déplacement
        elif event.keysym == "space":
            bombe = poser_bombe(etat_jeu["carte"], etat_jeu["joueur_x"], etat_jeu["joueur_y"])
            if bombe:
                etat_jeu["bombes"].append(bombe)

    fenetre.bind("<KeyPress>", deplacer_joueur)
    dessiner_carte()
    decrementer_timer()
    gestion_bombes()
    gerer_apparition_fantomes()
    gestion_fantomes()
