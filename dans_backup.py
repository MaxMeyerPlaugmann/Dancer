import pgzrun
from pgzero.actor import Actor
from pgzero import keyboard
from random import randint

BREDD = 800
HOJD = 600
MITT_X = BREDD / 2
MITT_Y = HOJD / 2

steglista = []
visa_lista = []

summa = 0
aktuellt_steg = 0
antal = 4
danslangd = 4

ropa_dansa = False
visa_nedrakning = True
steg_klara = False
spelet_slut = False

dansare = Actor("dancer-start")
dansare.pos = MITT_X + 5, MITT_Y - 40

upp = Actor("up")
upp.pos = MITT_X, MITT_Y + 110

hoger = Actor("right")
hoger.pos = MITT_X + 60, MITT_Y + 170

ner = Actor("down")
ner.pos = MITT_X, MITT_Y + 230

vanster = Actor("left")
vanster.pos = MITT_X - 60, MITT_Y + 170

def draw():
    global spelet_slut, summa, ropa_dansa   
    global antal,visa_nedrakning
    if not spelet_slut:
        screen.clear()
        screen.blit("stage", (0, 0))
        dansare.draw()
        upp.draw()
        ner.draw()
        hoger.draw()
        vanster.draw()
        screen.draw.text("Summa:" +
                         str(summa), color="black",
                         topleft=(10, 10))
    return


pgzrun.go()