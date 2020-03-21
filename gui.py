import pyglet
import random
import game
import ai

WIN_WITH = 900
WIN_HEIGHT = 500

win = pyglet.window.Window(WIN_WITH, WIN_HEIGHT, resizable=False)
pics = {}
state = {
    "state": 0, # 0=place ship horizontally, 1=place ship vertically, 2=player turn, 3=computer turn, 4=game over
    "ship": 1, # 1=first ship, 2=second ship ... used to place ships
    "ai": None
}

def load_pics(path):
    pyglet.resource.path = [path]
    pics["miss"] = pyglet.resource.image("square_red.png")
    pics["hit"] = pyglet.resource.image("square_green.png")
    pics["empty"] = pyglet.resource.image("square_back.png")
    pics["ship"] = pyglet.resource.image("square_x.png")
    pics["rotate"] = pyglet.resource.image("rotate.png")
    pics["new"] = pyglet.resource.image("new_game.png")

def write_text(text, x, y):
    label = pyglet.text.Label(text, 
    font_name='Times New Roman',
    font_size=18,
    x=x, y=y,)
    label.draw()

def draw_squares(boardP, boardC_show):
    batch = pyglet.graphics.Batch()
    sprites = []
    for j, row in enumerate(boardP):
        for i, square in enumerate(row):
            if square == ' ':
                x = i * 40
                y = (WIN_HEIGHT -140) - j * 40
                sprites.append(pyglet.sprite.Sprite(pics["empty"], x, y, batch=batch))
            elif square == '$':
                x = i * 40
                y = (WIN_HEIGHT -140) - j * 40
                sprites.append(pyglet.sprite.Sprite(pics["hit"], x, y, batch=batch))
            elif square == '*':
                x = i * 40
                y = (WIN_HEIGHT -140) - j * 40
                sprites.append(pyglet.sprite.Sprite(pics["miss"], x, y, batch=batch))
            else:
                x = i * 40
                y = (WIN_HEIGHT -140) - j * 40
                sprites.append(pyglet.sprite.Sprite(pics["ship"], x, y, batch=batch))
        
    for j, row in enumerate(boardC_show):
        for i, square in enumerate(row):
            if square == ' ':
                x = i * 40 + 450
                y = (WIN_HEIGHT -140) - j * 40
                sprites.append(pyglet.sprite.Sprite(pics["empty"], x, y, batch=batch))
            elif square == '$':
                x = i * 40 + 450
                y = (WIN_HEIGHT -140) - j * 40
                sprites.append(pyglet.sprite.Sprite(pics["hit"], x, y, batch=batch))
            elif square == '*':
                x = i * 40 + 450
                y = (WIN_HEIGHT -140) - j * 40
                sprites.append(pyglet.sprite.Sprite(pics["miss"], x, y, batch=batch))
        
    batch.draw()
    sprites.clear()

def draw_message():
    if state["state"] == 1:
        text = "Place your ship vertically"
        write_text(text, 0, 450)
        rotate = pyglet.sprite.Sprite(pics["rotate"], x=280, y=410)
        rotate.draw()
    elif state["state"] == 0:
        text = "Place your ship horizontally"
        write_text(text, 0, 450)
        rotate = pyglet.sprite.Sprite(pics["rotate"], x=280, y=410)
        rotate.draw()
    else:
        text = game.game["player_last"]
        write_text(text, 450, 450)
        text2 = game.game["com_last"]
        write_text(text2, 0, 450)
    
    if state["state"] == 4:
        rotate = pyglet.sprite.Sprite(pics["new"], x=280, y=410)
        rotate.draw()

def click_place_ship(x,y):
    height = 10
    x_fixed = x // 40 
    y_fixed = height - y // 40 -1
    if state["ship"] == 1:
        size = 2
        orient = state["state"]
        if game.validate_placement(x_fixed, y_fixed, orient, size, game.game["boards"]["boardP"]):
            game.place_ship(x_fixed, y_fixed, orient, 'a', game.game["boards"]["boardP"])
            state["ship"] = 2
    elif state["ship"] == 2:
        size = 3
        orient = state["state"]
        if game.validate_placement(x_fixed, y_fixed, orient, size, game.game["boards"]["boardP"]):
            game.place_ship(x_fixed, y_fixed, orient, 'b', game.game["boards"]["boardP"])
            state["ship"] = 3
    elif state["ship"] == 3:
        size = 3
        orient = state["state"]
        if game.validate_placement(x_fixed, y_fixed, orient, size, game.game["boards"]["boardP"]):
            game.place_ship(x_fixed, y_fixed, orient, 'c', game.game["boards"]["boardP"])
            state["ship"] = 4
    elif state["ship"] == 4:
        size = 4
        orient = state["state"]
        if game.validate_placement(x_fixed, y_fixed, orient, size, game.game["boards"]["boardP"]):
            game.place_ship(x_fixed, y_fixed, orient, 'd', game.game["boards"]["boardP"])
            state["ship"] = 5
    elif state["ship"] == 5:
        size = 5
        orient = state["state"]
        if game.validate_placement(x_fixed, y_fixed, orient, size, game.game["boards"]["boardP"]):
            game.place_ship(x_fixed, y_fixed, orient, 'e', game.game["boards"]["boardP"])
            state["state"] = random.randint(2,3) # Randomly choose player or computer start

def click_fire(x,y,board):
    height = 10
    x_fixed = (x - 450) // 40
    y_fixed = height - y // 40 -1

    response = game.make_move(board, x_fixed, y_fixed)

    if response == 'miss':
        state["state"] = 3
        board[y_fixed][x_fixed] = '*'
        game.game["boards"]["boardC_show"][y_fixed][x_fixed] = '*'
        game.game["player_last"] = "Missed"
    elif response == 'hit':
        state["state"] = 3
        if game.check_sunk(board, x_fixed, y_fixed, "computer_ships"):
            game.game["player_last"] = "Hit and sunk"
        else:
            game.game["player_last"] = "Hit"
        board[y_fixed][x_fixed] = '$'
        game.game["boards"]["boardC_show"][y_fixed][x_fixed] = '$'

def rotate_click(x,y):
    if x > 280 and y > 410 and x < 430 and y < 470:
        return True
    return False

def board_click(x,y):
    if x > 0 and y > 0 and x < 400 and y < 400:
        return True
    return False

def radar_click(x,y):
    if x > 450 and y > 0 and x < 850 and y < 400:
        return True
    return False

def player_won():
    # Returns true or false
    sum = 0
    for ship in game.game["computer_ships"]:
        sum += game.game["computer_ships"][ship]
    if sum == 0:
        return True

    sum = 0
    for ship in game.game["player_ships"]:
        sum += game.game["player_ships"][ship]
    if sum == 0:
        return False

def new_game():
    game.game["boards"]["boardP"] = game.create_board()
    game.game["boards"]["boardC"] = game.create_board()
    game.game["boards"]["boardC_show"] = game.create_board()
    game.game["player_last"] = "Game on"
    game.game["com_last"] = ""
    game.game["player_ships"]["a"] = 2
    game.game["player_ships"]["b"] = 3
    game.game["player_ships"]["c"] = 3
    game.game["player_ships"]["d"] = 4
    game.game["player_ships"]["e"] = 5
    game.game["computer_ships"]["a"] = 2
    game.game["computer_ships"]["b"] = 3
    game.game["computer_ships"]["c"] = 3
    game.game["computer_ships"]["d"] = 4
    game.game["computer_ships"]["e"] = 5
    game.ai_place_ships()
    state["ai"] = ai.Ai()
    state["ship"] = 1
    state["state"] = 0

@win.event
def on_mouse_press(x, y, btn, modifiers):
    if btn == pyglet.window.mouse.LEFT:
        #print(x,y)
        if state["state"] == 0:
            if rotate_click(x, y):
                state["state"] = 1
            elif board_click(x,y):
                click_place_ship(x, y)
        elif state["state"] == 1:
            if rotate_click(x, y):
                state["state"] = 0
            elif board_click(x,y):
                click_place_ship(x, y)
        elif state["state"] == 2:
            if radar_click(x, y):
                click_fire(x, y, game.game["boards"]["boardC"])
        
        if state["state"] == 3 and game.game_on():
            state["ai"] = game.computer_guess(game.game["boards"]["boardP"], state["ai"])
            if game.game_on():
                state["state"] = 2

        if state["state"] == 4 and rotate_click(x, y):
            new_game()
        
        if not game.game_on():
            state["state"] = 4
            if player_won():
                game.game["player_last"] = "Game over, player won"
            else:
                game.game["player_last"] = "Game over, computer won"

@win.event
def on_draw():
    win.clear()
    write_text("Your board", 0,410)
    write_text("Your radar", 450,410)
    draw_message()
    draw_squares(game.game["boards"]["boardP"], game.game["boards"]["boardC_show"])

if __name__ == "__main__":
    load_pics("sprites")
    new_game()

    pyglet.app.run()