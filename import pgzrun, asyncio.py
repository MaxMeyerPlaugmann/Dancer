import pgzrun, asyncio
from random import randint

# Skärmstorlek
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

# Speldata
step_list = []
show_list = []

score = 0
current_step = 0
count = 4
dance_length = 4

say_dance = False
show_countdown = True
steps_done = False
game_over = False

# Skapa aktörer
dancer = Actor("dancer-start")
dancer.pos = CENTER_X + 5, CENTER_Y - 40

up = Actor("up")
up.pos = CENTER_X, CENTER_Y + 110

right = Actor("right")
right.pos = CENTER_X + 60, CENTER_Y + 170

down = Actor("down")
down.pos = CENTER_X, CENTER_Y + 230

left = Actor("left")
left.pos = CENTER_X - 60, CENTER_Y + 170

def draw():
    screen.clear()
    screen.blit("stage", (0, 0))
    screen.draw.text("Poäng: " + str(score), color="black", topleft=(10, 10))

    if game_over:
        screen.draw.text("SPELET ÄR SLUT!", color="black",
                         topleft=(CENTER_X - 170, 220), fontsize=60)
        screen.draw.text("Tryck [MELLANSLAG] för att spela igen", color="black",
                         topleft=(CENTER_X - 250, 300), fontsize=40)
    else:
        dancer.draw()
        up.draw()
        down.draw()
        right.draw()
        left.draw()

        if say_dance:
            screen.draw.text("Dansa!", color="black",
                             topleft=(CENTER_X - 65, 150), fontsize=60)
        elif show_countdown:
            screen.draw.text(str(count), color="black",
                             topleft=(CENTER_X - 8, 150), fontsize=60)

def dancer_back():
    if not game_over:
        dancer.image = "dancer-start"
        up.image = "up"
        right.image = "right"
        down.image = "down"
        left.image = "left"

def update_dancer(step):
    if not game_over:
        if step == 0:
            up.image = "up-lit"
            dancer.image = "dancer-up"
        elif step == 1:
            right.image = "right-lit"
            dancer.image = "dancer-right"
        elif step == 2:
            down.image = "down-lit"
            dancer.image = "dancer-down"
        else:
            left.image = "left-lit"
            dancer.image = "dancer-left"
        clock.schedule(dancer_back, 0.5)

def show_steps():
    global show_list, say_dance, show_countdown
    if show_list:
        this_step = show_list.pop(0)
        update_dancer(this_step)
        clock.schedule(show_steps, 1)
    else:
        say_dance = True
        show_countdown = False

def create_steps():
    global step_list, show_list, count, say_dance, show_countdown
    count = 4
    step_list = []
    show_list = []
    say_dance = False
    for i in range(dance_length):
        step = randint(0, 3)
        step_list.append(step)
        show_list.append(step)
    show_countdown = True
    countdown()

def countdown():
    global count, show_countdown
    if count > 1:
        count -= 1
        clock.schedule(countdown, 1)
    else:
        show_countdown = False
        show_steps()

def next_step():
    global current_step, steps_done
    if current_step < dance_length - 1:
        current_step += 1
    else:
        steps_done = True

def on_key_up(key):
    global score, current_step, game_over
    if say_dance and not game_over:
        if key == keys.UP:
            update_dancer(0)
            if step_list[current_step] == 0:
                score += 1
                next_step()
            else:
                game_over = True
        elif key == keys.RIGHT:
            update_dancer(1)
            if step_list[current_step] == 1:
                score += 1
                next_step()
            else:
                game_over = True
        elif key == keys.DOWN:
            update_dancer(2)
            if step_list[current_step] == 2:
                score += 1
                next_step()
            else:
                game_over = True
        elif key == keys.LEFT:
            update_dancer(3)
            if step_list[current_step] == 3:
                score += 1
                next_step()
            else:
                game_over = True

def on_key_down(key):
    if game_over and key == keys.SPACE:
        restart_game()

def restart_game():
    global score, current_step, count, step_list, show_list
    global say_dance, show_countdown, steps_done, game_over

    score = 0
    current_step = 0
    count = 4
    step_list = []
    show_list = []
    say_dance = False
    show_countdown = True
    steps_done = False
    game_over = False

    create_steps()
    music.play("vanishing-horizon")

def update():
    global steps_done, current_step
    if steps_done and not game_over:
        create_steps()
        current_step = 0
        steps_done = False
    elif game_over:
        music.stop()

async def main(): 
    # Starta spelet
    create_steps()
    music.play("vanishing-horizon")

    pgzrun.go()
    await asyncio.sleep(0)  # Allow the event loop to run


asyncio.run(main())
# This code is a simple rhythm game where the player must press the correct arrow keys in time with a sequence of dance steps.
# The game features a dancer actor that changes its image based on the player's input, and a countdown before the dance sequence starts.
# The player earns points for each correct step and the game ends if an incorrect step is pressed.
# The game can be restarted by pressing the space key after a game over.
# The game uses the Pygame Zero library for graphics and input handling, and it includes a music track that plays during the game.
# The game is designed to be simple and engaging, with a focus on timing and memory for the dance steps.
# The game is structured to allow for easy modifications, such as changing the dance sequence length or the images used for the dancer and directions.
# The game also includes a countdown feature to build anticipation before the dance sequence begins.
# The code is structured to be easily readable and maintainable, with clear function definitions for each part of the game logic.
# The game is designed to be played with a keyboard, using the arrow keys for input.
# The game is suitable for players of all ages and can be enjoyed as a fun and interactive way to test rhythm and memory skills.
# The game can be extended with additional features, such as different dance sequences, more complex input patterns, or visual effects.
# The game is a good example of how to use Pygame Zero for creating interactive games with simple mechanics and engaging visuals.
# This code is a simple rhythm game where the player must press the correct arrow keys in time with a sequence of dance steps.
# The game features a dancer actor that changes its image based on the player's input, and a countdown before the dance sequence starts.
# The player earns points for each correct step and the game ends if an incorrect step is pressed.
# The game can be restarted by pressing the space key after a game over.
# The game uses the Pygame Zero library for graphics and input handling, and it includes a music track that plays during the game.
# The game is designed to be simple and engaging, with a focus on timing and memory for the dance steps.
# The game is structured to allow for easy modifications, such as changing the dance sequence length or the images used for the dancer and directions.ls

