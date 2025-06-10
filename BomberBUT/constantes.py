# Timers pour le jeu
TIMER_GLOBAL = 250  # Nombre de tours avant la fin du jeu
TIMER_FANTOME = 20  # Nombre de tours entre l'apparition de nouveaux fantômes

PV_INITIAL = 3  # Nombre de points de vie initiaux pour le joueur


# Carte initiale
CARTE_INITIALE = [
    "CCCCCCCCCCCCCCCCCCCCC",
    "C E                 C",
    "C C C C C C C C C C C",
    "C MMMMMMMMMMMMMMMMM C",
    "C CMCMCMCMCMCMCMCMC C",
    "C MMMMMMMMMMMMMMMMM C",
    "C CMCMCMCMCMCMCMCMC C",
    "C MMMMMMMMMMMMMMMMM C",
    "C CMCMCMCMCMCMCMCMC C",
    "C MMMMMMMMMMMMMMMMM C",
    "C CMCMCMCMCMCMCMCMC C",
    "C        P          C",
    "C CMCMCMCMCMCMCMCMC C",
    "C MMMMMMMMMMMMMMMMM C",
    "C CMCMCMCMCMCMCMCMC C",
    "C MMMMMMMMMMMMMMMMM C",
    "C CMCMCMCMCMCMCMCMC C",
    "C MMMMMMMMMMMMMMMMM C",
    "C CMCMCMCMCMCMCMCMC C",
    "C                 E C",
    "CCCCCCCCCCCCCCCCCCCCC"
]

# Taille des cases en pixels
TAILLE_CASE = 30

# Couleurs pour représenter les éléments du jeu
COULEURS = {
    "C": "gray",     # Murs incassables
    "M": "brown",    # Murs cassables
    "E": "green",    # Prises Ethernet
    "P": "blue",     # Personnage
    "F": "purple",   # Fantômes
    "B": "orange",   # Bombes
    " ": "green",    # Cases vides
}

