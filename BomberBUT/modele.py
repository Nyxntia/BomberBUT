import random

def trouver_joueur(carte):
    """Trouve la position initiale du joueur sur la carte."""
    for y, ligne in enumerate(carte):
        for x, case in enumerate(ligne):
            if case == "P":
                return x, y

def bouger_joueur(carte, x, y, direction):
    """Déplace le joueur dans une direction donnée si la case est accessible."""
    dx, dy = 0, 0
    if direction == "haut":
        dy = -1
    elif direction == "bas":
        dy = 1
    elif direction == "gauche":
        dx = -1
    elif direction == "droite":
        dx = 1

    nx, ny = x + dx, y + dy  # Calculer les nouvelles coordonnées

    if (
        0 <= ny < len(carte) and 0 <= nx < len(carte[0]) and
        carte[ny][nx] not in ["C", "M", "F"]   #Verification limites et cases bloquantes
    ):
        if carte[y][x] == "P":
            carte[y][x] = " " # Remplacement de l'ancienne case du joueur

        if carte[ny][nx] != "E":
            carte[ny][nx] = "P"   # Si la case n'est pas une prise Ethernet alors la case est remplacée par "P"
        return nx, ny

    return x, y

def poser_bombe(carte, x, y):
    """Place une bombe sur la carte, sauf sur une prise Ethernet."""
    if carte[y][x] in ["B"]:  # Bombe déjà présente
        return None
    elif carte[y][x] == "E":  # Interdire de poser une bombe sur une prise Ethernet
        return None
    else:  # Bombe sur une case normale
        carte[y][x] = "B"
        return (x, y, 5)  # Minuteur initial

def diminuer_timers(bombes):
    """Réduit les timers des bombes."""
    return [(x, y, timer - 1) for x, y, timer in bombes if timer > 1]

def faire_exploser(carte, x, y, score, portee, joueur_pos=None, etat_jeu=None, deja_explosees=None):
    """Gère l'explosion d'une bombe et ses effets."""
    if deja_explosees is None:
        deja_explosees = set()

    if (x, y) in deja_explosees:
        return score
    deja_explosees.add((x, y))

    directions = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
    for dx, dy in directions:
        for distance in range(1, portee + 1):
            nx, ny = x + dx * distance, y + dy * distance

            if 0 <= ny < len(carte) and 0 <= nx < len(carte[0]):
                case = carte[ny][nx]

                # Si l'explosion touche une prise Ethernet, ne rien faire
                if case == "E":
                    break

                # Si l'explosion touche le joueur
                if joueur_pos == (nx, ny) and etat_jeu is not None:
                    etat_jeu["pv"] -= 1
                    print(f"Le joueur a été touché par une explosion ! PV restants : {etat_jeu['pv']}")
                    if etat_jeu["pv"] <= 0:
                        print("Game Over !")
                        print(f"Score atteint : {etat_jeu['score']}")
                        etat_jeu["jeu_actif"] = False
                        etat_jeu["fenetre"].destroy()
                        return score

                if case == "C":  # Mur incassable
                    break
                elif case == "M":  # Mur cassable
                    carte[ny][nx] = " "
                    score += 1
                elif case == "F":  # Fantôme
                    carte[ny][nx] = " "
                    if etat_jeu is not None:
                        etat_jeu["fantomes"] = [
                            (fx, fy) for fx, fy in etat_jeu["fantomes"] if (fx, fy) != (nx, ny)
                        ]
                    score += 10
                elif case == "B":  # Bombe en chaîne
                    carte[ny][nx] = " "
                    score = faire_exploser(
                        carte, nx, ny, score, portee, joueur_pos, etat_jeu, deja_explosees
                    )
                else:  # Case vide ou autre
                    if joueur_pos != (nx, ny):  # Ne pas modifier la case où se trouve le joueur
                        carte[ny][nx] = " "

    # Vérification de victoire
    if etat_jeu and all("M" not in ligne for ligne in carte):
        print("Victoire ! Tous les murs ont été détruits.")
        print(f"Score final : {etat_jeu['score']}")
        etat_jeu["jeu_actif"] = False
        etat_jeu["fenetre"].destroy()

    return score

def apparition_fantomes(carte):
    """Génère des fantômes autour des prises Ethernet."""
    nouvelles_positions = []
    for y, ligne in enumerate(carte):
        for x, case in enumerate(ligne):
            if case == "E":
                cases_vides = [
                    (x + dx, y + dy)
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    if 0 <= x + dx < len(carte[0]) and 0 <= y + dy < len(carte) and carte[y + dy][x + dx] == " "
                ]
                if cases_vides:
                    nx, ny = random.choice(cases_vides)
                    carte[ny][nx] = "F"
                    nouvelles_positions.append((nx, ny))
    return nouvelles_positions

def deplacer_fantomes(carte, fantomes, joueur_x, joueur_y, etat_jeu):
    """Déplace les fantômes sur la carte tout en vérifiant les collisions avec le joueur."""
    nouvelles_positions = []
    bombes = etat_jeu["bombes"]

    for fx, fy in fantomes:
        if abs(fx - joueur_x) + abs(fy - joueur_y) == 1:
            etat_jeu["pv"] -= 1
            print(f"Collision avec un fantôme ! PV restants : {etat_jeu['pv']}")
            if etat_jeu["pv"] <= 0:
                print("Game Over ! Le joueur a perdu tous ses PV.")
                print(f"Score atteint : {etat_jeu['score']}")
                etat_jeu["jeu_actif"] = False
                etat_jeu["fenetre"].destroy()
                return nouvelles_positions # Arrêt immédiat si le jeu est terminé
            nouvelles_positions.append((fx, fy)) # Ajout de la position actuelle à la liste des nouvelles positions
            continue  # Traitement du fantôme s'arrête

        if bombes:
            cible_bombe = min(bombes, key=lambda b: abs(fx - b[0]) + abs(fy - b[1]))  # Calcul de la bombe la plus proche
            bx, by, _ = cible_bombe   # Coordonnées de la bombe la plus proche
            directions = [
                (fx + dx, fy + dy)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Directions possibles du fantôme
                if (
                    0 <= fx + dx < len(carte[0]) and
                    0 <= fy + dy < len(carte) and
                    carte[fy + dy][fx + dx] in [" ", "P"]  # La case doit être non bloquante
                )
            ]
            if directions:
                directions.sort(key=lambda d: abs(d[0] - bx) + abs(d[1] - by))  # Calcul de la direction pour se rapprocher au maximum de la bombe
                nx, ny = directions[0]   # La première direction est choisie comme destination pour le fantôme
            else:
                nx, ny = fx, fy     # Si aucune direction est disponible le fantôme reste sur place
        else:                       #Si aucune bombe présente sur la carte
            directions = [
                (fx + dx, fy + dy)
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                if (
                    0 <= fx + dx < len(carte[0]) and
                    0 <= fy + dy < len(carte) and
                    carte[fy + dy][fx + dx] in [" ", "P"]
                )
            ]
            if directions:
                nx, ny = random.choice(directions)   # Le fantôme se déplace de manière aléatoire
            else:
                nx, ny = fx, fy   # Si aucune case accessible le fantôme reste sur place

        if carte[ny][nx] != "P": #Empêche l'écrasement du joueur
            carte[fy][fx] = " "  #Fantôme disparaît de sa position
            carte[ny][nx] = "F"  #Fantôme apparaît dans sa nouvelle position

        nouvelles_positions.append((nx, ny))

    return nouvelles_positions   # Liste des nouvelles positions
