import matplotlib.pyplot as plot

pieces = [("Vide", 0), ("Porte-Avion", 5), ("Croiseur", 4), ("Contre-Torpilleur", 3), ("Sous-Marin", 3), ("Torpilleur", 2)]
plateau = [[0 for i in range(10)] for i in range(10)]

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
        print("Wrong input for the board")
        return False
    
    if (bateau not in range(6)):
        print("Wrong input for the ship")
        return False
    
    if (position[0]<0 or position[0]>9 or position[1]<0 or position[1]>9):
        print("Unauthorized position")
        return False

    if (direction not in [1,2]):
        print("Unauthorized direction")
        return False

    if (direction == 1):
        for i in range(pieces[bateau][1]):
            if (position[1]+i>9):
                print("Out of bounds")
                return False
            if (grille[position[0], position[1]+i]!=0):
                print("Ship already in place")
                return False
        return True

    if (direction == 2):
        for i in range(pieces[bateau][1]):
            if (position[0]+i>9):
                print("Out of bounds")
                return False
            if (grille[position[0]+i, position[1]]!=0):
                print("Ship already in place")
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
        
        if(direction == 2):
            for i in range(pieces[bateau][1]):
                grille[position[0]+i][position[1]] = bateau
        
        print("The ship has been deployed!")
    
    else:
        print("Can't deploy ship")
    

def affiche(grille):
    plot.imshow(grille)
    plot.show()

affiche(plateau)
