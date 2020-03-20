"""
Battleship boardgame

@author: Eetu Karvonen

Notes:

Empty square = ' '
Ship square = 'a' or 'b' or 'c'...

orient horizontal = 0
orient vertical = 1

"""

import random
import time
import ai

game = {
    "boards": {
        "boardP": [],
        "boardC": [],
        "boardC_show": []
    },
    
    "player_ships": {
        "a": 2,
        "b": 3,
        "c": 3,
        "d": 4,
        "e": 5
    },
    "computer_ships": {
        "a": 2,
        "b": 3,
        "c": 3,
        "d": 4,
        "e": 5
    },
    "turn": 0,          # Computers turn 0, players turn 1
    "player_last": "",  # Used to print last moves, 'missed', 'hit' or 'hit and sunk'
    "com_last": ""
}

def create_board():
    # Create empty board

    board = []

    for i in range(10):
        i = i # To avoid "unused variable" -warning
        board_row = []
        for j in range(10):
            j = j # To avoid "unused variable" -warning
            board_row.append(' ')
        
        board.append(board_row)
    
    return board

def ai_place_ships():

    for key in game["computer_ships"]:

        size = game["computer_ships"][key]

        # Randomly place ships
        x_coord = random.randint(0,9)
        y_coord = random.randint(0,9)
        orient = random.randint(0,1)

        # If placement is not valid, create new placement as long as it is valid
        while not validate_placement(x_coord, y_coord, orient, size, game["boards"]["boardC"]):
            x_coord = random.randint(0,9)
            y_coord = random.randint(0,9)
            orient = random.randint(0,1)
            
        place_ship(x_coord, y_coord, orient, key, game["boards"]["boardC"])
        
def player_place_ships():

    for key in game["player_ships"]:
        # Ask player where to place ships
        size = game["player_ships"][key]
        print("Where do you want to place a ship sized ", size)
        x, y, orient = ask_placement(size) # ask_placement() also validates placement

        place_ship(x, y, orient, key, game["boards"]["boardP"])

        print_board()
        
def place_ship(x,y,orient,ship,board):
    # Place a single ship. Call after validated placement

    if orient == 0:
        for i in range(game["player_ships"][ship]):
            board[y][x+i] = ship
    elif orient == 1:
        for i in range(game["player_ships"][ship]):
            board[y+i][x] = ship

    return board

def validate_placement(x,y,orient,size,board):
    # Checks if ship can be placed to x,y. Returns true or false

    if x < 0 or y < 0:
        return False

    if orient == 0 and x + size > 10:
        return False
    elif orient == 1 and y + size > 10:
        return False
    else:
        if orient == 0:
            for i in range(size):
                if board[y][x+i] != ' ':
                    return False
        elif orient == 1:
            for i in range(size):
                if board[y+i][x] != ' ':
                    return False

    return True

def ask_placement(size):
    # Ask player where to place a ship and which direction
    while True:
        try:
            x_coord = int(input("Give x-coordinate: ")) - 1
            y_coord = int(input("Give y-coordinate: ")) - 1
            orient = input("Place ship (v)ertically or (h)orizontally: ")
            print(" ")
            
            if orient != 'v' and orient != 'h':
                raise Exception("Invalid input, enter v or h")

            if orient == 'v':
                orient = 1
            else:
                orient = 0
            
            if x_coord > 9 or x_coord < 0 or y_coord > 9 or y_coord < 0:
                raise Exception("Invalid input. Please use values between 1 to 10 only.")

            if validate_placement(x_coord, y_coord, orient, size, game["boards"]["boardP"]):
                return x_coord, y_coord, orient
            else:
                raise Exception("Can't place a ship there, try again")

        except ValueError:
            print("Invalid input, enter a number between 1 and 10")
            continue
        except Exception as e:
            print(e)
            continue

def computer_guess(board,comp_ai):
    move = comp_ai.pick_move()
    x = move[0] - 1
    y = move[1] - 1
    response = make_move(board, x, y)
    
    if response == 'miss':
        board[y][x] = '*'
        game["com_last"] = "Missed"
        
    elif response == 'hit':
        comp_ai.hit(x+1, y+1)
        if check_sunk(board, x, y, "player_ships"):
            game["com_last"] = "Hit and sunk"
            comp_ai.hits = []
        else:
            game["com_last"] = "Hit"
        board[y][x] = '$'
    print("Computer: ", game["com_last"]) # Prints 'Missed', 'Hit', or 'Hit and sunk'
    return comp_ai

def player_guess(board):
    while True:
        try:
            x = int(input("Give x-coordinate you want to hit: ")) - 1
            y = int(input("Give y-coordinate you want to hit: ")) - 1
            if x < 0 or x > 9 or y < 0 or y > 9:
                raise ValueError
        except ValueError:
            print("Invalid input, enter a number between 1 and 10")
            continue
        
        
        response = make_move(board, x, y)
        
        if response == 'again':
            print("You have already fired there, try again")
            continue
        elif response == 'miss':
            board[y][x] = '*'
            game["boards"]["boardC_show"][y][x] = '*'
            game["player_last"] = "Missed"
            break
        elif response == 'hit':
            if check_sunk(board, x, y, "computer_ships"):
                game["player_last"] = "Hit and sunk"
            else:
                game["player_last"] = "Hit"
            board[y][x] = '$'
            game["boards"]["boardC_show"][y][x] = '$'
            break

def make_move(board,x,y):
    if board[y][x] == ' ':
        return 'miss'
    elif board[y][x] == '*' or board[y][x] == '$':
        return 'again'
    else:
        return 'hit'
    
def check_sunk(board,x,y,opponent):
    ship = board[y][x]
    game[opponent][ship] -= 1
    return game[opponent][ship] == 0

def print_board():
    print("Your board")
    for row in game["boards"]["boardP"]:
        print(row)
    print(" ")

def print_radar():
    print("Your radar")
    for row in game["boards"]["boardC_show"]:
        print(row)
    print(" ")

def game_on():
    # Checks if all ships are sunk

    sum = 0
    for ship in game["computer_ships"]:
        sum += game["computer_ships"][ship]
    if sum == 0:
        return False

    sum = 0
    for ship in game["player_ships"]:
        sum += game["player_ships"][ship]
    if sum == 0:
        return False
    return True

def play():
    game["turn"] = random.randint(0,1)  # Randomly choose which start
    comp_ai = ai.Ai()                   # Init ai

    if game["turn"] == 0:
        print("Computer starts")
    else:
        print("You start")

    while game_on():
        if game["turn"] == 0:
            # Computer's turn
            comp_ai = computer_guess(game["boards"]["boardP"], comp_ai)
            game["turn"] = 1
        else:
            # Player's turn
            print(" ")
            print_board()
            print_radar()
            player_guess(game["boards"]["boardC"])
            game["turn"] = 0
            print("You: ", game["player_last"]) # Prints 'Missed', 'Hit', or 'Hit and sunk'

if __name__ == "__main__":
    game["boards"]["boardP"] = create_board()
    game["boards"]["boardC"] = create_board()
    game["boards"]["boardC_show"] = create_board()

    print("Welcome to play battleships")
    print(" ")

    ai_place_ships()
    player_place_ships()

    play()

    print("Game over")
    if game["turn"] == 0:
        print("Player won")
        print("")
        print_radar()
    else:
        print("Computer won")
        print("")
        print_board()
