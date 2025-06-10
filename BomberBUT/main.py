from graphique.vues import initialiser_jeu
from constantes import CARTE_INITIALE, TIMER_GLOBAL, TIMER_FANTOME
import tkinter as tk

def main():
    # Initialisation de la fenêtre principale
    fenetre = tk.Tk()
    fenetre.title("BomberBUT")

    # Initialisation du jeu avec les constantes
    initialiser_jeu(fenetre, CARTE_INITIALE, TIMER_GLOBAL, TIMER_FANTOME)

    # Lancement boucle principale
    fenetre.mainloop()

if __name__ == "__main__":
    main()
