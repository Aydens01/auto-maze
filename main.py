
# On importe la bibliothèque 'random'.
from random import *

#############
#-FONCTIONS-#__Nous avons ici l'ensemble des fonctions utilisées dans la création du labyrinthe.
#############

# Etat des fonctions :
"""
1°  creation     : ok
2°  wall         : ok
3°  verification : ok
4°  end          : supprimée
5°  brokenWall   : ok
6°  update       : ok
7°  graphic      : ok
8°  in_out       : ok
9°  check        : ok
10° street       : ok
11° starter      : ok
12° contagion    : ok
13° followTheWay : ok
14° begin        : ok
15° way          : ok
"""


## Génération de la matrice labyrinthe ##-----------------------------------------------------


#----- Créer la matrice labyrinthe à son premier état :

def creation(largeur, hauteur) :
    # on initialise une matrice et un compteur.
    matrix, count =  [], 0
    # création de la matrice suivant les données fournis par l'utilisateur.
    for l in range(2*hauteur+1) :
        # initialisation d'une ligne de la matrice.
        ligne = []
        # répartition des -1 et des valeurs positives dans la matrice.
        if l%2==0 :
            ligne = [-1 for c in range(2*largeur+1)]
        else :
            for c in range(2*largeur+1) :
                if c%2==0 :
                    ligne.append(-1)
                else :
                    ligne.append(count)
                    count += 1
        matrix.append(ligne)
    # On retourne notre matrice de départ.
    return(matrix)

#----- Créer une liste des coordonnées(ligne, colonne) des murs cassables :

def wall(largeur, hauteur, matrice) :
    # On initialise notre liste.
    wall = []
    # On parcourt la matrice
    for l in range(1, 2*hauteur) :
        for c in range(1, 2*largeur) :
            # Tout mur vérifiant les conditions requises voit ses coordonnées ajoutées à la liste.
            if verification(l, c, matrice) :
                wall.append([l, c])
    # On retourne la liste des murs cassables.
    return(wall)

#----- Déterminer si le mur peut être détruit :

def verification(l, c, matrice) :
    # On vérifie que la case du haut ou de gauche ne soit pas un mur.
    if matrice[l-1][c]!=-1 or matrice[l][c-1]!=-1 :
        # Si oui, on retourne True.
        return(True)
    else :
        # Sinon, on retourne False.
        return(False)

#----- Détruit un mur et renvoie les valeurs positives maximum et minimum des cases adjacentes :

def brokenWall(liste, matrice) :
    # On crée un booléen qui indiquera si un mur a été cassé.
    ajout = False
    # On prend aléatoirement un mur dans la liste des murs cassables.
    index=randint(0, len(liste)-1)
    mur = liste[index]
    # On récupère ses coordonées.
    l, c = int(mur[0]), int(mur[1])
    # On distingue deux cas : le mur est dans une ligne impaire ou dans une ligne paire

    if l%2!=0 :
        # Si la ligne est impaire, il suffit d'étudier les valeurs à droite et à gauche du mur.
        # On trouve la valeur maximale et la valeur minimale.
        maxi=max(matrice[l][c-1],matrice[l][c+1])
        mini=min(matrice[l][c-1],matrice[l][c+1])
        # La condition suivante empêche la création de plusieurs chemins.
        # Ainsi on produit un labyrinthe parfait.
        if maxi!=mini :
            # La case du mur prend la valeur minimale.
            matrice[l][c]=mini
            # Notre booléen 'ajout' devient True.
            ajout = True
        # On retire le mur choisi de la liste des murs cassables.
        liste.pop(index)

    else :
        # Si la ligne est paire, on étudie les valeurs en haut et en bas du mur.
        # On récupère le maximum et le minimum de ces deux cases.
        maxi=max(matrice[l-1][c],matrice[l+1][c])
        mini=min(matrice[l-1][c],matrice[l+1][c])
        # Même principe que précédemment.
        if maxi!=mini :
            matrice[l][c]=mini
            ajout = True
        # On retire le mur choisi de la liste des murs cassables.
        liste.pop(index)

    # On retourne le maximum, le minimum, la liste des murs cassables et la matrice.
    return(maxi, mini, liste, matrice, ajout)

#----- Actualiser les données de la matrice labyrinthe :

def update(maxi, mini, matrice) :
    # On lit la matrice labytinthe
    for i in range(len(matrice)) :
        for j in range(len(matrice[i])) :

            # Si on trouve la valeur maxi, on la remplace par la valeur mini.
            if matrice[i][j] == maxi :
                matrice[i][j] = mini

    # On retourne notre matrice mise à jour.
    return(matrice)


## Contrôle de l'affichage du labyrinthe sur le terminal ##-----------------------------------


# Image colorée pour Linux.
def graphic(matrice) :
    # lecture de la matrice
    for i in range(len(matrice)) :
        # On crée une chaine de caractère qui représente un ligne de la matrice.
        lab =""
        for j in range(len(matrice[i])):
            # Création graphique des zones de passage en blanc.
            if matrice[i][j]==0 :
                lab=lab + '\x1b[0;30;47m' + "  " + '\x1b[0m'
            # Création graphique des murs en bleu.
            elif matrice[i][j]==-1 :
                lab=lab + '\x1b[0;30;44m' + "  " + '\x1b[0m'
            # Création graphique du chemin le plus court en rouge.
            elif matrice[i][j]=="-5" or matrice[i][j]==1 :
                lab = lab + '\x1b[0;31;41m' + "  " +'\x1b[0m'
            # Création graphique de l'entrée.
            elif matrice[i][j]=="-2" :
                lab = lab + "A "
            # Création graphique de la sortie.
            elif matrice[i][j]=="-3" :
                lab = lab + "B "
            # Gérer les autres caractères.
            else :
                lab = lab + '\x1b[0;30;47m' + "  " + '\x1b[0m'
        # On affiche la ligne juste créée.
        print(lab)

# Affichage basique.
def sobre(matrice) :
    # Lecture de la matrice
    for i in range(len(matrice)) :
        # On crée une chaine de caractère qui représente un ligne de la matrice.
        lab =""
        for j in range(len(matrice[i])):
            # Création graphique des zones de passage.
            if matrice[i][j]==0 :
                lab=lab + "  "
            # Création graphique des murs.
            elif matrice[i][j]==-1 :
                lab=lab + "* "
            # Création graphique du chemin le plus court.
            elif matrice[i][j]=="-5" or matrice[i][j]==1 :
                lab = lab + "¤ "
            # Création graphique de l'entrée.
            elif matrice[i][j]=="-2" :
                lab = lab + "A "
            # Création graphique de la sortie.
            elif matrice[i][j]=="-3" :
                lab = lab + "B "
            # Gérer les autres caractères.
            else :
                lab = lab + "  "
        # On affiche la ligne juste créée.
        print(lab)


## Création de l'entrée et de la sortie du labyrinthe ##--------------------------------------


def in_out(matrice) :
    # On demande à l'uilisateur les coordonnées du point de départ.
    print("Entrer les coordonnées du point de départ :")
    entree_x = int(input("X : "))
    entree_y = int(input("Y : "))
    # Si l'entrée est mal placée (fonction check qui renvoie Faux), on demande
    # à l'utilisateur de recommencer la saisie des coordonnées.
    while not check(entree_x, entree_y, matrice) :
        print("Les coordonnées sont incorrectes.")
        print("Entrer les coordonnées du point de départ :")
        entree_x = int(input("X : "))
        entree_y = int(input("Y : "))
    # On attribue dans la matrice, la valeur -2 à l'entrée.
    matrice[entree_y][entree_x]="-2"

    # On demande à l'uilisateur les coordonnées du point d'arrivée.
    print("Entrer les coordonées du point de d'arrivée :")
    sortie_x = int(input("X : "))
    sortie_y = int(input("Y : "))
    # Si la sortie est mal placée (fonction check qui renvoie Faux), on demande
    # à l'utilisateur de recommencer la saisie des coordonnées.
    while not check(sortie_x, sortie_y, matrice) :
        print("Les coordonnées sont incorrectes.")
        print("Entrer les coordonnées du point d'arrivée :")
        sortie_x = int(input("X : "))
        sortie_y = int(input("Y : "))
    # On attribue dans la matrice, la valeur -3 à l'entrée.
    matrice[sortie_y][sortie_x]="-3"

    # On retourne les coordonnées de l'entrée et de la sortie, ainsi que la matrice.
    return([entree_y, entree_x], [sortie_y, sortie_x], matrice)

#----- Vérification des coordonnées des ouvertures sur les bords du dédale.
#----- Analysons les différentes conditions :

def check(x, y, matrice) :

    #/ 1° : mur de gauche sans les angles avec la vérification qu'il
    #/ n'y a pas de murs directement sur la droite de la position.

    if x==0 and y!=0 and matrice[y][x+1]==0 :
        # Si oui, retourne True.
        return(True)

    #/ 2° : mur du haut sans les angles avec la vérification qu'il n'y a pas de
    #/ murs directement en bas de la position.

    elif x!=0 and y==0 and matrice[y+1][x]==0 :
        # Si oui, retourne True.
        return(True)

    #/ 3° : mur de droite sans les angles avec la vérification qu'il n'y a pas de
    #/ murs directement sur la gauche de la position.

    elif x==len(matrice[y])-1 and y!=len(matrice)-1 and matrice[y][x-1]==0 :
        # Si oui, retourne True.
        return(True)

    #/ 4° : mur du bas sans les angles avec la vérification qu'il n'y a pas de
    #/ murs directement en haut de la position.

    elif y==len(matrice)-1 and x!=len(matrice[y]) and matrice[y-1][x]==0 :
        # Si oui, retourne True.
        return(True)
    else :
        # Sinon, retourne False.
        return(False)


## Résolution de la matrice labyrinthe ##-----------------------------------------------------


# On remplit la matrice labyrinthe avec des valeurs croissantes en partant de l'entrée :

def street(entree, sortie, matrice) :
    # On place le chiffre 1 à l'entrée du labyrinthe.
    starter(entree, matrice)
    # Initialisation du compteur.
    count = 0
    # On crée une liste qui contiendra les coordonnées
    # des cases où nous devons appliquer notre fonction contagion.
    memory=[starter(entree, matrice)]
    # Booléen qui met fin à la propagation si la sortie a été trouvée.
    fin = False
    # Booléen qui indique si la sortie a été trouvée.
    booleen = False
    # Boucle d'exploration du labyrinthe.
    while not fin :
        # Liste qui retient les cases qui ont changés de valeurs.
        memory2 = []
        #On incrélente notre compteur de 1.
        count+=1
        # On parcourt la liste des cases récemment explorées.
        for i in range(len(memory)):
            # On applique notre fonction contagion.
            memory2, booleen = contagion(memory[i], count, matrice, memory)
            # Si la sortie est trouvée alors on indique la fin de la boucle avec
            # le booléen fin.
            if booleen == True :
                fin = booleen
        # On retient les cases dernièrement explorées.
        memory = memory2

    # On retourne la dernière valeur du compteur
    return(count)

# Détection de la sortie, retourne un booléen.
def detection(couple, matrice) :
    # On analyse les 4 cases adjacentes.
    if matrice[couple[0]][couple[1]+1]=="-3" or matrice[couple[0]+1][couple[1]]=="-3" or matrice[couple[0]][couple[1]-1]=="-3" or matrice[couple[0]-1][couple[1]]=="-3":
        # Si la sortie est l'une de ces cases, retourne True.
        return(True)
    else :
        # Sinon, retourne False.
        return(False)

# Prend en argument les coordonnées de l'entrée et la matrice.
# Retourne la position de la case devant l'entrée.
def starter(entree, matrice) :

    # On place le 1 en fonction de la position de l'entrée et on retourne les
    # coordonnées de la première case.

    # Si l'entrée est sur le bord de gauche.
    if entree[0] == 0 :
        matrice[entree[0]+1][entree[1]]=1
        return([entree[0]+1, entree[1]])

    # Si l'entrée est sur le bord de droite.
    elif entree[0] == len(matrice)-1 :
        matrice[entree[0]-1][entree[1]]=1
        return([entree[0]-1, entree[1]])

    # Si l'entrée est sur le bord du haut.
    elif entree[1] == 0 :
        matrice[entree[0]][entree[1]+1]=1
        return([entree[0], entree[1]+1])

    # Si l'entrée est sur le bord du bas.
    elif entree[1] == len(matrice)-1 :
        matrice[entree[0]][entree[1]-1]=1
        return([entree[0], entree[1]-1])

# Prend en arguments un couple, un entier positif, la matrice et une liste.
# Retourne la liste contenant les coordonnées des prochaines cases à explorer.
def contagion(couple, count, matrice,liste) :
    # Le couple contient les coordonnées de la case sur laquelle nous sommes.

    # Si la case de droite n'est pas un mur et est inexplorée.
    if matrice[couple[0]][couple[1]+1]==0 :
        # La case prend la valeur du compteur + 1.
        matrice[couple[0]][couple[1]+1]=count+1
        # On ajoute les coordonnées de la case dans la liste.
        liste.append([couple[0],couple[1]+1])
    # Si la case du bas n'est un mur et est inexplorée.
    if matrice[couple[0]+1][couple[1]]==0:
        # La case prend la valeur du compteur + 1.
        matrice[couple[0]+1][couple[1]]=count+1
        # On ajoute les coordonnées de la case dans la liste.
        liste.append([couple[0]+1, couple[1]])
    # Si la case de gauche n'est pas un mur et est inexplorée.
    if matrice[couple[0]][couple[1]-1]==0:
        # La case prend la valeur du compteur + 1.
        matrice[couple[0]][couple[1]-1]=count+1
        # On ajoute les coordonnées de la case dans la liste.
        liste.append([couple[0], couple[1]-1])
    # Si la case du haut n'est pas un mur et est inexplorée.
    if matrice[couple[0]-1][couple[1]]==0:
        # La case prend la valeur du compteur + 1.
        matrice[couple[0]-1][couple[1]]=count+1
        # On ajoute les coordonnées de la case dans la liste.
        liste.append([couple[0]-1, couple[1]])
    # Si la sortie est repérée .
    if detection(couple, matrice) :
        # On retourne la nouvelle liste et True.
        return(liste, True)
    # On retourne la nouvelle liste et False.
    return(liste, False)

#----- Trouver le chemin le plus court.
# Prend en arguments les coordonnées de l'entrée et de la sortie, ainsi que le compteur et la matrice.
def followTheWay(entree, sortie, count, matrice) :
    # On commence à la sortie du labyrinthe
    coor = begin(matrice)
    while not matrice[coor[0]][coor[1]] == 1  : # tant qu'on n'a pas trouvé l'entrée.
        # On navigue dans le labyrinthe en créant le chemin.
        coor = way(coor, count, matrice)
        # On diminue le compteur de 1.
        count-=1

# Fonction qui renvoie les coordonnées de la case avant la sortie du labyrinthe.
def begin(matrice) :
    # On parcourt la matrice.
    for l in range(len(matrice)):
        for c in range(len(matrice[l])) :
            # Si la case est adjacente à la sortie et que sa valeur est égale au précédent compteur.
            if matrice[l][c]==count and detection([l, c], matrice):
                # On retourne les coordonnées de la case trouvée.
                return([l, c])

# Prend en arguments, des coordonnées, un compteur et la matrice.
def way(couple, count, matrice) :
# On part des coordonnées données par le couple.

    # Si la valeur du mur de droite est inférieure strictement à la valeur de la case actuelle tout en étant strictement positive.
    if 0<int(matrice[couple[0]][couple[1]+1])<count :
        # La case prend la valeur -5.
        matrice[couple[0]][couple[1]]="-5"
        # Et on retourne les coordonnées de la case trouvée.
        return([couple[0], couple[1]+1])
    # Si la valeur du mur du bas est inférieure strictement à la valeur de la case actuelle tout en étant strictement positive.
    elif 0<int(matrice[couple[0]+1][couple[1]])<count :
        # La case prend la valeur -5.
        matrice[couple[0]][couple[1]]="-5"
        # Et on retourne les coordonnées de la case trouvée.
        return([couple[0]+1, couple[1]])
    # Si la valeur du mur de gauche est inférieure strictement à la valeur de la case actuelle tout en étant strictement positive.
    elif 0<int(matrice[couple[0]][couple[1]-1])<count :
        # La case prend la valeur -5.
        matrice[couple[0]][couple[1]]="-5"
        # Et on retourne les coordonnées de la case trouvée.
        return([couple[0], couple[1]-1])
    # Si la valeur du mur du haur est inférieure strictement à la valeur de la case actuelle tout en étant strictement positive.
    elif 0<int(matrice[couple[0]-1][couple[1]])<count :
        # La case prend la valeur -5.
        matrice[couple[0]][couple[1]]="-5"
        # Et on retourne les coordonnées de la case trouvée.
        return([couple[0]-1, couple[1]])


#############
#-PROGRAMME-#
#############

if __name__=="__main__":
    # I/ Initialisation :

    # L'utilisateur rentre les dimensions de la matrice de départ.
    l = int(input("Saisissez la largeur :"))
    h = int(input("Saisissez la hauteur :"))
    print("Il est conseillé de choisir un affichage sobre sur tout système d'exploitation autre que Linux.")
    aff=input("Souhaitez-vous un affichage sobre du labyrinthe ? (y/n) :")
    # On crée la matrice labyrinthe.
    matrice = creation(l, h)

    # II/ Etapes 1-->n :

    # On fait une liste des murs cassables.
    liste_murs = wall(l, h, matrice)
    # Compteur des murs que l'on a cassé.
    compteur = 0
    # On crée un booléen qui indiquera si un mur a été cassé.
    ajout = False

    # On crée aléatoirement un labyrinthe.
    # l*h-1 est le nombre de murs que l'on doit casser pour faire un labyrinthe parfait.
    while compteur < l*h-1:
        # On casse des murs.
        maxi, mini,liste_murs, matrice, ajout = brokenWall(liste_murs, matrice)

        if ajout == True :
            # On incrémente le compteur de 1
            compteur += 1
            # On mets à jour notre matrice labyrinthe.
            matrice = update(maxi, mini, matrice)

    # On affiche le labyrinthe aléatoire généré.
    print("Voici le labyrinthe aléatoire généré :")
    # On affiche le labyrinthe sous la forme qu'a choisi l'utilisateur.
    if aff=='y' :
        sobre(matrice)
    else :
        graphic(matrice)

    # III / Recherche du plus court chemin :

    # L'utilisateur rentre les coordonnées de l'entrée et de la sortie du labyrinthe.
    entree, sortie, matrice = in_out(matrice)

    # On cherche le plus court chemin pour résoudre le labyrinthe :

    # On explore le labyrinthe.
    count = street(entree, sortie, matrice)
    # On repère le plus court chemin
    followTheWay(entree, sortie, count, matrice)
    # On affiche le labyrinthe avec sa meilleure solution.
    print("Voici le plus court chemin :")
    # On affiche le labyrinthe sous la forme qu'a choisi l'utilisateur.
    if aff=='y' :
        sobre(matrice)
    else :
        graphic(matrice)
