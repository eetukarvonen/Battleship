"""
Ai Class for battleship game

@author Eetu Karvonen

Ai.pick_move() returns a move Ai chooses

Implemntation of AI is really complicated
Logic goes as following:

- "available_moves" list contains every square as a tuple (x,y). When ai fires a square,
move is removed from the list
- If ai hits, hit is added to "hits" list, when sink happens "hits" empties. 
Hit is also added to "permanent_hits" list which does not empty when sink happens

- If there is no previous hit, ai chooses move randomly from the list "random_moves" which contains
only every other squeare. There is no need to go through every squeare becouse no ship can
fit into area if every other square is bombarded

- If there is 1 previous hit, ai fires squares next to it (funcition find_next())

- If there is 2 previous hits, ai finds the "hit_orient", which is (r)ight, (d)own (l)eft or (u)p
and chooses move with function "find_according_orient()"

- If there is more than 2 previous hits move is chosen with function find_according_orient()

- find_according_orient function chooses square next to last hit, according the orient. 
If move is not available, direction is changed. Lastly if move is still not found, 
function "find_next_perm_hits()" is called. That function will go through "permanent_hits" list
and finds the move next to previous hits.

"""

import random

class Ai:
    available_moves = []
    random_moves = []
    hits = []
    permanent_hits = []
    hit_orient = 'l' # Which direction to seek when found hit. (r)ight, (d)own (l)eft or (u)p 

    def __init__(self):
        for i in range(1,11):
            for j in range(1,11):
                if i % 2 == j % 2:  # Only every other move is added to random moves
                    self.random_moves.append((i,j))
                    self.available_moves.append((i,j))
                else:
                    self.available_moves.append((i,j))

    def pick_move(self):
        move_number = None
        if len(self.hits) == 0: # No previous hits
            rand_move_number = random.randint(0,len(self.random_moves)-1)
            move = self.random_moves.pop(rand_move_number)

            for i in range(len(self.available_moves)):
                # Finds the move number of the move
                if move == self.available_moves[i]:
                    move_number = i
        else:
            if len(self.hits) == 1:
                hit = self.hits[0]
                move = self.find_next(hit)

                for i in range(len(self.random_moves)):
                    # Removes the move from random_moves
                    if move == self.random_moves[i]:
                        self.random_moves.pop(i)
                        break

                for i in range(len(self.available_moves)):
                    # Finds the move number of the move
                    if move == self.available_moves[i]:
                        move_number = i
                        break

            elif len(self.hits) == 2:
                self.find_dir()
                move_number = self.find_according_orient()
            elif len(self.hits) > 2:
                move_number = self.find_according_orient()

        if move_number == None:
            move_number = self.find_next_perm_hits()
            
        return self.available_moves.pop(move_number)
    
    def find_next(self, hit):
        # Iterates squares next to hit, check if move is available and return the move
        for neighbour in range(-1,2,2): # range(start=-1, stop=2, interval=2), x = -1 and x = 1
            x = hit[0]
            y = hit[1]
            move = (x+neighbour, y)
            if move in self.available_moves:
                return move
            move = (x, y+neighbour)
            if move in self.available_moves:
                return move

    def find_dir(self):
        # Called when two hits. 
        # Compares first and second hit and finds the orientation
        prev_hit = self.hits[0]
        hit = self.hits[1]
        x = hit[0]
        y = hit[1]
        prev_x = prev_hit[0]
        prev_y = prev_hit[1]

        if prev_x == x:                 # hits are vertical
            if prev_y > y:              # we hitted above previous
                self.hit_orient = 'u'
            else:                       # we hitted belows previous
                self.hit_orient = 'd'
        elif prev_y == y:               # hits are horizontal
            if prev_x > x:              # we hitted left to previous
                self.hit_orient = 'l'
            else:                       # we hitted right to previous
                self.hit_orient = 'r'

    def find_according_orient(self):
        prev_hit = self.hits[-1]

        if self.hit_orient == 'u':
            move = (prev_hit[0], (prev_hit[1] -1))
        elif self.hit_orient == 'd':
            move = (prev_hit[0], (prev_hit[1] +1))
        elif self.hit_orient == 'l':
            move = (prev_hit[0] -1, prev_hit[1])
        elif self.hit_orient == 'r':
            move = (prev_hit[0] +1, prev_hit[1])

        for i in range(len(self.available_moves)):
            # Finds the move number of the move
            if move == self.available_moves[i]:
                for j in range(len(self.random_moves)):
                    # Removes the move from random_moves
                    if move == self.random_moves[j]:
                        self.random_moves.pop(j)
                        return i
                return i
        
        # Move not available, change direction
        if self.hit_orient == 'u':
            self.hit_orient = 'd'
        elif self.hit_orient == 'd':
            self.hit_orient = 'u'
        elif self.hit_orient == 'l':
            self.hit_orient = 'r'
        elif self.hit_orient == 'r':
            self.hit_orient = 'l'

        first_hit = self.hits[0]
        if self.hit_orient == 'u':
            move = (first_hit[0], (first_hit[1] -1))
        elif self.hit_orient == 'd':
            move = (first_hit[0], (first_hit[1] +1))
        elif self.hit_orient == 'l':
            move = (first_hit[0] -1, first_hit[1])
        elif self.hit_orient == 'r':
            move = (first_hit[0] +1, first_hit[1])

        for i in range(len(self.available_moves)):
            # Finds the move number of the move
            if move == self.available_moves[i]:
                for j in range(len(self.random_moves)):
                    # Removes the move from random_moves
                    if move == self.random_moves[j]:
                        self.random_moves.pop(j)
                        return i
                return i

        # If move still not available, change vertical to horizontal and horizontal to vertical
        if self.hit_orient == 'u':
            self.hit_orient = 'r'
        elif self.hit_orient == 'd':
            self.hit_orient = 'l'
        elif self.hit_orient == 'l':
            self.hit_orient = 'u'
        elif self.hit_orient == 'r':
            self.hit_orient = 'd'

        if self.hit_orient == 'u':
            move = (prev_hit[0], (prev_hit[1] -1))
        elif self.hit_orient == 'd':
            move = (prev_hit[0], (prev_hit[1] +1))
        elif self.hit_orient == 'l':
            move = (prev_hit[0] -1, prev_hit[1])
        elif self.hit_orient == 'r':
            move = (prev_hit[0] +1, prev_hit[1])

        for i in range(len(self.available_moves)):
            # Finds the move number of the move
            if move == self.available_moves[i]:
                for j in range(len(self.random_moves)):
                    # Removes the move from random_moves
                    if move == self.random_moves[j]:
                        self.random_moves.pop(j)
                        return i
                return i
        
        # Still move not available
        return self.find_next_perm_hits()

    def find_next_perm_hits(self):
        # Go through all last hits and check squares next to hit
        for k in range(len(self.permanent_hits)-1, -1, -1): # Loop permanent_hits backwards
            hit = self.permanent_hits[k]
            move = self.find_next(hit)
            for i in range(len(self.available_moves)):
                # Finds the move number of the move
                if move == self.available_moves[i]:
                    for j in range(len(self.random_moves)):
                        # Removes the move from random_moves
                        if move == self.random_moves[j]:
                            self.random_moves.pop(j)
                            return i
                    return i

    def hit(self,x,y):
        # Called when hitted at (x,y)
        # Adds hit to list
        hit = (x,y)
        self.hits.append(hit)
        self.permanent_hits.append(hit)
