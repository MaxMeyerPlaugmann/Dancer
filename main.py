import pgzrun
from random import randint

# Skærmindstillinger
WIDTH = 800
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

# Spilvariable
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

goku_unlocked = False  # Låses op efter 50 point eller cheat
right_streak = 0      # Til cheat-koden

# Hent billede af danseren afhængig af direction og om Goku er låst op
def get_dancer_image(direction="start"):
    if goku_unlocked:
        return "dancer-goku-default" if direction == "start" else f"dancer-goku-{direction}"
    if direction == "start":
        return "dancer-start"
    return f"dancer-{direction}"

# Skab aktører (sprites)
def create_actors():
    global dancer, up, right, down, left
    dancer = Actor(get_dancer_image("start"))
    dancer.pos = (CENTER_X + 5, CENTER_Y - 40)

    up = Actor("up")
    up.pos = (CENTER_X, CENTER_Y + 110)

    right = Actor("right")
    right.pos = (CENTER_X + 60, CENTER_Y + 170)

    down = Actor("down")
    down.pos = (CENTER_X, CENTER_Y + 230)

    left = Actor("left")
    left.pos = (CENTER_X - 60, CENTER_Y + 170)

create_actors()

def draw():
    screen.clear()
    screen.blit("stage", (0, 0))
    screen.draw.text("Poäng: " + str(score), color="black", topleft=(10, 10))
    if goku_unlocked:
        screen.draw.text("GOKU UNLOCKED!", color="fuchsia", topleft=(CENTER_X-200, 10), fontsize=60)

    if game_over:
        screen.draw.text("SPELET ÄR SLUT!", color="black",
                         topleft=(CENTER_X - 170, 220), fontsize=60)
        screen.draw.text("Tryck [MELLANSLAG] för at spela igen", color="black",
                         topleft=(CENTER_X - 250, 300), fontsize=40)
    else:
        dancer.draw()
        up.draw()
        down.draw()
        right.draw()
        left.draw()
        if show_countdown:
            screen.draw.text(str(count), color="black", topleft=(CENTER_X - 8, 150), fontsize=60)
        if say_dance:
            screen.draw.text("Dansa!", color="black", topleft=(CENTER_X - 65, 100), fontsize=60)

def dancer_back():
    if not game_over:
        dancer.image = get_dancer_image("start")
        up.image = "up"
        right.image = "right"
        down.image = "down"
        left.image = "left"

def update_dancer(step):
    if not game_over:
        if step == 0:
            up.image = "up-lit"
            dancer.image = get_dancer_image("up")
        elif step == 1:
            right.image = "right-lit"
            dancer.image = get_dancer_image("right")
        elif step == 2:
            down.image = "down-lit"
            dancer.image = get_dancer_image("down")
        elif step == 3:
            left.image = "left-lit"
            dancer.image = get_dancer_image("left")
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
    global step_list, show_list, count, say_dance, show_countdown, current_step
    count = 4
    step_list = []
    show_list = []
    say_dance = False
    for i in range(dance_length):
        step = randint(0, 3)
        step_list.append(step)
        show_list.append(step)
    show_countdown = True
    current_step = 0
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
    global score, current_step, game_over, goku_unlocked, steps_done, right_streak, dancer

    # Cheat-kode: tryk højre 4 gange under nedtælling
    if show_countdown:
        if key == keys.RIGHT:
            right_streak += 1
            if right_streak == 4 and not goku_unlocked:
                goku_unlocked = True
                dancer.image = get_dancer_image("start")  # Vis GOKU straks
        else:
            right_streak = 0
        return

    # Normalt spil
    if say_dance and not game_over:
        correct = False

        if key == keys.UP:
            update_dancer(0)
            correct = step_list[current_step] == 0
            right_streak = 0  # Reset streak under dans
        elif key == keys.RIGHT:
            update_dancer(1)
            correct = step_list[current_step] == 1
            right_streak = 0
        elif key == keys.DOWN:
            update_dancer(2)
            correct = step_list[current_step] == 2
            right_streak = 0
        elif key == keys.LEFT:
            update_dancer(3)
            correct = step_list[current_step] == 3
            right_streak = 0

        if correct:
            score += 1
            if score >= 20 and not goku_unlocked:
                goku_unlocked = True
                dancer.image = get_dancer_image("start")  # Vis GOKU straks
            next_step()
        else:
            game_over = True

def on_key_down(key):
    if game_over and key == keys.SPACE:
        restart_game()

def restart_game():
    global score, current_step, count, step_list, show_list
    global say_dance, show_countdown, steps_done, game_over, right_streak, goku_unlocked
    goku_unlocked = False
    create_actors()
    score = 0
    current_step = 0
    count = 4
    step_list = []
    show_list = []
    say_dance = False
    show_countdown = True
    steps_done = False
    game_over = False
    right_streak = 0 
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

create_steps()
music.play("vanishing-horizon")

pgzrun.go()
