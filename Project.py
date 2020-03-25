import time
import matplotlib.pyplot as plot
import random 
import copy

pieces = [("Vide", 0), ("Porte-Avion", 5), ("Croiseur", 4), ("Contre-Torpilleur", 3), ("Sous-Marin", 3), ("Torpilleur", 2)]
pieces_1 = [("Vide", 0), ("Porte-Avion", 5)]
pieces_2 = [("Vide", 0), ("Porte-Avion", 5), ("Croiseur", 4)]
pieces_3 = [("Vide", 0), ("Porte-Avion", 5), ("Croiseur", 4), ("Contre-Torpilleur", 3)]
plateau_vide = [[0 for i in range(10)] for i in range(10)]

def peut_placer(grille, bateau, position, direction):
    """
    Checks if we can deploy a ship
    input:  
        int[][] grille:
            Game board, first index is lines, second is columns.
        int bateau:
            Type of ship as defined in tab "plateau"         
        (int, int) position:
            Upper left position of the first square that the boat will occupy
        int direction:
            Direction in which the ship will be placed:
            - 1 for horizontal
            - 2 for vertical
    """

    if (not grille):
        #print("Wrong input for the board")
        return False
    
    if (bateau not in range(6)):
        #print("Wrong input for the ship")
        return False
    
    if (position[0]<0 or position[0]>9 or position[1]<0 or position[1]>9):
        #print("Unauthorized position")
        return False

    if (direction not in [1,2]):
        #print("Unauthorized direction")
        return False

    if (direction == 1):
        for i in range(pieces[bateau][1]):
            if (position[1]+i>9):
                #print("Out of bounds")
                return False
            if (grille[position[0]][position[1]+i]!=0):
                #print("Ship already in place")
                return False
        return True

    if (direction == 2):
        for i in range(pieces[bateau][1]):
            if (position[0]+i>9):
                #print("Out of bounds")
                return False
            if (grille[position[0]+i][position[1]]!=0):
                #print("Ship already in place")
                return False
        return True

def place(grille, bateau, position, direction):
    """
    Deploys a ship.
    input:  
        int[][] grille:
            Game board, first index is lines, second is columns.
        int bateau:
            Type of ship as defined in tab "plateau"         
        (int, int) position:
            Upper left position of the first square that the boat will occupy
        int direction:
            Direction in which the ship will be placed:
            - 1 for horizontal
            - 2 for vertical
    """
    
    if(peut_placer(grille, bateau, position, direction)):
        if(direction == 1):
            for i in range(pieces[bateau][1]):
                grille[position[0]][position[1]+i] = bateau
            return True
        
        if(direction == 2):
            for i in range(pieces[bateau][1]):
                grille[position[0]+i][position[1]] = bateau
            return True
        #print("The ship has been deployed!")
    
    else:
        #print("Can't deploy ship")
        return False

def place_alea(grille, bateau):
    """
    Deploys a ship randomly
    input:  
        int[][] grille:
            Game board, first index is lines, second is columns.
        int bateau:
            Type of ship as defined in tab "plateau"
    """ 
    p = (random.randint(0, 9), random.randint(0,9))
    d = random.randint(1, 2)
    while peut_placer(grille, bateau, p, d) == False:
        p = (random.randint(0, 9), random.randint(0,9))
        d = random.randint(1, 2)
    place(grille, bateau, p, d)

def affiche(grille):
    plot.imshow(grille)
    plot.show()

def eq(grilleA, grilleB):
    """
    Check if the game boards are identical
    input:
        int[][] grilleA:
            Game board number one
        int[][] grilleB:
            Game board number two
    """
    return grilleA == grilleB

def genere_grille():
    """ 
    generate the game board with randomly deployed ships
    """
    grille = [[0 for i in range(10)] for i in range(10)]
    for bateau in range(1,len(pieces)):
        place_alea(grille, bateau)
    return grille
    
def denobrement_bateau(bateau, grille):
    nb = 0
    size = len(grille)
    for i in range(size):
        for j in range(size):
            if peut_placer(grille, bateau, (i,j), 1):
                nb+=1
            if peut_placer(grille, bateau, (i,j), 2):
                nb+=1
    return nb

def denobrement_liste_bateau(liste_bateau, grille, bateau=1):
    nb = 0
    size = len(grille)
    for i in range(size):
        for j in range(size):
            if peut_placer(grille, bateau, (i,j), 1):
                if (bateau==len(liste_bateau)-1):
                    nb+=1
                else:
                    gc = copy.deepcopy(grille)
                    place(gc, bateau, (i,j), 1)
                    nb += denobrement_liste_bateau(liste_bateau, gc, bateau+1)
            if peut_placer(grille, bateau, (i,j), 2):
                if (bateau==len(liste_bateau)-1):
                    nb+=1
                else:
                    gc = copy.deepcopy(grille)
                    place(gc, bateau, (i,j), 2)
                    nb += denobrement_liste_bateau(liste_bateau, gc, bateau+1)
    return nb

def nb_grille(grille):
    nb = 0
    p = eq(grille, genere_grille())
    while(not p):
        nb += 1
        p = eq(grille, genere_grille())
    return nb

class Bataille:
    def __init__(self, plateau = genere_grille()):
        self.alive = 5
        self.grille = plateau
        self.pieces = [("Vide", 0), ("Porte-Avion", 5), ("Croiseur", 4), ("Contre-Torpilleur", 3), ("Sous-Marin", 3), ("Torpilleur", 2)]
        self.positions_pieces = {self.pieces[i][0] : set() for i in range(len(pieces))} 
        self.touched = {self.pieces[i][0] : set() for i in range(len(pieces))}
        size = len(self.grille)
        for i in range(size):
            for j in range(size):
                self.positions_pieces[self.pieces[self.grille[i][j]][0]].add((i,j))

    def joue(self, position):
            bateau = self.grille[position[0]][position[1]]
            self.touched[self.pieces[bateau][0]].add(position)
            if bateau > 0:
                if self.touched[self.pieces[bateau][0]] == self.positions_pieces[self.pieces[bateau][0]]:
                    print("Coulé!")
                    self.alive -= 1
                    return (self.victoire(),2)
                else:
                    print("Touché!")
                    return (self.victoire(),1)
            return (False, 0)
    
    def victoire(self):
        if self.alive == 0:
            print("VICTOIRE!")
            return True
        return False
    
    def reset(self):
        self.alive = 5
        self.touched = {self.pieces[i][0] : set() for i in range(len(pieces))}

class Joueur_Alea:
    def __init__(self):
        self.vict = False
        self.played = set()
    def joue(self, bataille):
        turns = 0
        while (not self.vict):
            turns += 1
            self.vict = self.tour(bataille)[0]
        return turns
    def tour(self, bataille):
        position = (random.randint(0,9), random.randint(0,9))
        while position in self.played:
            position = (random.randint(0,9), random.randint(0,9))
        self.played.add(position)
        return bataille.joue(position)

class Joueur_heuristique:
    
    def __init__(self):
        self.vict=False
        self.played = set()
        last_pos = (0,0)
    def joue(self, bataille):
        turns = 0
        found = 0
        direction = 0
        while (not self.vict):
            turn = self.tour(bataille, found, direction)
            if (self.last_pos not in self.played):
                self.played.add(self.last_pos)
                turns+=1
            if (found>0):
                if turn[1]==0:
                    direction = (direction + 1)%4
                elif found == 2:
                    found = 0
            self.vict = turn[0]
        return turns
    
    def tour(self, bataille, found, direction):
        
        if found==0:

            position = (random.randint(0,9), random.randint(0,9))
            curr_turn = bataille.joue(position)
            self.last_pos = position
            return curr_turn

        else:
            #Up
            if bataille.direction == 0:
                position = self.last_pos
                if position[0]>0:
                    position[0] = position[0]-1
                else: 
                    bataille.direction = (bataille.direction + 1)%4

            #Right
            if bataille.direction == 1:
                position = self.last_pos
                if position[1]<9:
                    position[1] = position[1]+1
                else: 
                    bataille.direction = (bataille.direction + 1)%4
            #Down
            if bataille.direction == 2:
                position = self.last_pos
                if position[0]<9:
                    position[0] = position[0]+1
                else: 
                    bataille.direction = (bataille.direction + 1)%4
            #Left
            if bataille.direction == 3:
                position = self.last_pos
                position[1] = position[1]-1
            self.last_pos = position

            return bataille.joue(position)     


bat = Bataille()

print(bat.positions_pieces[bat.pieces[1][0]])
affiche(bat.grille)

dumbo = Joueur_Alea()
kindasm = Joueur_heuristique()
#print(dumbo.joue(bat))
#bat.reset()
print(kindasm.joue(bat))
