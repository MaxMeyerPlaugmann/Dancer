import pgzrun
from pgzero.actor import Actor
from pgzero import keyboard
from random import randint
from pgzero import clock

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
        if ropa_dansa:
            screen.draw.text("Dansa!", color="black",
                             topleft=(MITT_X - 65, 150), fontsize=60)
        if visa_nedrakning:
            screen.draw.text(str(antal), color="black",
                             topleft=(MITT_X - 8, 150), fontsize=60) 
    else:
        screen.clear()
        screen.blit("stage", (0, 0))  
        screen.draw.text("Summa:" + 
                        str(summa), color="black",
                        topleft=(10, 10)) 
        screen.draw.text("SLUTSPELAT!", color="black",
                        topleft=(MITT_X - 130, 220), fontsize=60)
    return    
            

def dansare_tillbaka():
    global spelet_slut
    if not spelet_slut:
        dansare.image = "dancer-start"
        upp.image = "up"
        hoger.image = "right"
        ner.image = "down"
        vanster.image = "left"
    return


def uppdatera_dansare(steg):
    global spelet_slut
    if not spelet_slut:
        if steg == 0:
            upp.image = "up-lit"
            dansare.image = "dancer-up"
            clock.schedule(dansare_tillbaka, 0.5)
        elif steg == 1:
            hoger.image = "right-lit"
            dansare.image = "dancer-right"
            clock.schedule(dansare_tillbaka, 0.5)
        elif steg == 2:
            ner.image = "down-lit"
            dansare.image = "dancer-down"
            clock.schedule(dansare_tillbaka, 0.5)
        else:
            vanster.image = "left-lit"
            dansare.image = "dancer-left"
            clock.schedule     (dansare_tillbaka, 0.5)
    return


def visa_steg():
    global steglista, visa_lista, danslangd
    global ropa_dansa, visa_nedrakning, aktuellt_steg   
    
    if visa_lista:
        detta_steg = visa_lista[0]
        visa_lista = visa_lista[1:]
        if detta_steg == 0:
            uppdatera_dansare(0)
            clock.schedule(visa_steg, 1)
        elif detta_steg == 1:
            uppdatera_dansare(1)
            clock.schedule(visa_steg, 1)
        elif detta_steg == 2:
            uppdatera_dansare(2)
            clock.schedule(visa_steg, 1)
        else:
            uppdatera_dansare(3)
            clock.schedule(visa_steg, 1)
    else:
        ropa_dansa = True
        visa_nedrakning = False
    return    


def skapa_steg():
    global steglista, danslangd, antal
    global visa_nedrakning, ropa_dansa
    antal = 4
    steglista = []
    ropa_dansa = False
    for steg in range(0, danslangd):
        slump_steg = randint(0, 3)
        steglista.append(slump_steg)
        visa_lista.append(slump_steg)
    visa_nedrakning = True
    nedrakning()
    return    


def nedrakning():
    global antal, spelet_slut, visa_nedrakning
    if antal > 1:
        antal = antal -1
        clock.schedule(nedrakning, 1)
    else:
        visa_nedrakning = False
        visa_steg()
    return        

def nasta_steg():
    pass

def on_key_up(key):
    global summa, spelet_slut, steglista, aktuellt_steg
    if key == keys.UP:
        uppdatera_dansare(0)
    elif key == keys.RIGHT:
        uppdatera_dansare(1)
    elif key == keys.DOWN:
        uppdatera_dansare(2)
    elif key == keys.LEFT:
        uppdatera_dansare(3)
    return                

skapa_steg()

def update():
    pass

pgzrun.go()