# -*- coding: utf-8 -*-

import pygame as pg
import sys
import math
import random

# Fikser pygame vindu
WIDTH = 600
HEIGHT = 400
SIZE = (WIDTH, HEIGHT)
pg.init()
surface = pg.display.set_mode(SIZE)
clock = pg.time.Clock()

GREEN = (76, 167, 114)
WHITE = (250, 250, 250)
LIGHTBLUE = (150, 120, 255)
BLACK = (0, 0, 0)
BROWN = (93, 71, 51)
GRAY = (100, 100, 100)

w = 20

sheeps = []
obsts = []
ghosts = []

# Klasse for alle karakterene
class Character():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        
    def draw(self):
        pg.draw.rect(surface, self.color, [self.x, self.y, w, w])
        
# Klasse for sau
class Sheep(Character):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        sheeps.append(self)
        self.carried = False
        
    def draw(self):
        if self.carried:
            pg.draw.rect(surface, self.color, [human.x+w/4, human.y+w/4, w, w])
        else:
            pg.draw.rect(surface, self.color, [self.x, self.y, w, w])
        
# Klasse for hindring    
class Obst(Character):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        obsts.append(self)

# Klasse for menneske
class Human(Character):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.speed = 5
        self.vx = self.speed
        self.vy = self.speed
        self.collission = False
    
    # Metode for forflytning
    def move(self):
        keys = pg.key.get_pressed()
        # Sjekker om tastene er trykket og endrer posisjonen
        if keys[pg.K_LEFT]:
            self.x -= self.speed
        if keys[pg.K_RIGHT]:
            self.x += self.speed
        if keys[pg.K_UP]:
            self.y -= self.speed
        if keys[pg.K_DOWN]:
            self.y += self.speed
        self.collision = False
            
        if self.x >= WIDTH-w:
            self.x = WIDTH-w
        if self.x <= 0:
            self.x = 0
        if self.y >= HEIGHT-w:
            self.y = HEIGHT-w
        if self.y <= 0:
            self.y = 0
            
    
    def pre_move(self):
        # Finner den neste posisjonen og returnerer om den kræsjer i neste frame
        x = self.x
        y = self.y
        
        collission = False
        
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            x -= self.speed
        if keys[pg.K_RIGHT]:
            x += self.speed
        if keys[pg.K_UP]:
            y -= self.speed
        if keys[pg.K_DOWN]:
            y += self.speed
            
        for u in obsts:
            if u.x+w > x and u.x < x+w and u.y+w > y and u.y < y+w:
                collission = True

        return collission
    
class Ghost(Character):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.speed = 2
        ghosts.append(self)
        
        # Gir lik fart i alle retninger
        self.vx = random.randint(-self.speed*10, self.speed*10)/10
        self.vy = (self.speed**2 - self.vx**2)**0.5
        if random.randint(0,1) < 0:
            self.vy *= -1

        
    def move(self):
        # Endrer posisjonen
        self.x += self.vx
        self.y += self.vy
        
        # Sjekker om den kræsjer i veggene på spillbrettert
        if self.x >= WIDTH-space-w:
            self.vx *= -1
        if self.x <= space:
            self.vx *= -1
        if self.y >= HEIGHT-w:
            self.vy *= -1
        if self.y <= 0:
            self.vy *= -1


space = 100

# Finner tilfeldige tall som ikke er oppå et annet objekt
def randomNr(startW, endW, startH, endH, n):
    randoms = []
    nrW = random.randint(startW, endW)
    nrH = random.randint(startH, endH)
    xy = [nrW, nrH]
    randoms.append(xy)
    
    while len(randoms) < n:
        nrW = random.randint(startW, endW)
        nrH = random.randint(startH, endH)
        xy = [nrW, nrH]
        duplicate = False
        for r in randoms:
            if nrW+w > r[0] and nrW < r[0]+w and nrH+w > r[1] and nrH < r[1]+w:
                duplicate = True
        if not duplicate:
            randoms.append(xy)
    return randoms

# Lager lister med tilfeldige tall til starten
randomO = randomNr(space, WIDTH-space-w, 0, HEIGHT-w, 3)
randomS = randomNr(WIDTH-space, WIDTH-w, 0, HEIGHT-w, 3)
        
# Lager objektene
for i in range(3): 
    obst = Obst(randomO[i][0], randomO[i][1], BROWN)
    
for i in range(3): 
    sheep = Sheep(randomS[i][0], randomS[i][1], WHITE)

human = Human(random.randint(0, space-w-5), random.randint(0, HEIGHT-w-5), BLACK)
ghost = Ghost(random.randint(space, WIDTH-space-w), random.randint(0, HEIGHT-w), LIGHTBLUE)

# Oppgaver kollisjon
def coll_det(u):
    if u.x+w > human.x and u.x < human.x+w and u.y+w > human.y and u.y < human.y+w:
        return True
    
# Viser tekst
def display_text(txt, txt_color, rect_color, x, y, s):
    font = pg.font.Font('freesansbold.ttf', s)
    text = font.render(txt, True, txt_color, rect_color)
    textRect = text.get_rect()
    textRect.center = (x, y)
    surface.blit(text, textRect)
    

run = True
 
FPS = 60
points = 0


while run:
    # Bilder per sekund
    clock.tick(FPS)
    
    # Gjør sånn at man kan avslutte vinduet
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    # Tilbakestiller brettet
    surface.fill(GRAY)
    
    # Lager gresset
    pg.draw.rect(surface, GREEN, [space, 0, WIDTH-2*space, HEIGHT])
        
    # Tegner hindringer
    for o in obsts:
        o.draw()
    
    doubleSheep = 0
    for s in sheeps:        
        s.draw()
        # Oppdager om en sau blir båret
        if coll_det(s):
            s.carried = True
            human.speed = 3
        if s.carried:
            doubleSheep += 1
        if doubleSheep >= 2:
            run = False
        
        # Alt som skal skje når spilleren får poeng
        if s.carried and human.x <= space:
            points += 1
            sheeps.remove(s)
            duplicateS = True
            duplicateO = True
            xS = 0
            yS = 0
            xO = 0
            yO = 0
            # Lager ny sau
            while duplicateS == True:
                human.speed = 6
                x = random.randint(WIDTH-space, WIDTH-w)
                y = random.randint(0, HEIGHT-w)
                duplicateS = False
                for s in sheeps:
                    if x+w > s.x and x < s.x+w and y+w > s.y and y < s.y+w:
                        duplicateS = True
            sheep = Sheep(x, y, WHITE)
            # Lager ny hindring
            while duplicateO == True:
                x = random.randint(space, WIDTH-space-w)
                y = random.randint(0, HEIGHT-w)
                duplicateO = False
                for o in obsts:
                    if x+w > o.x and x < o.x+w and y+w > o.y and y < o.y+w:
                        duplicateO = True
            obst = Obst(x, y, BROWN)
            #Lager nytt spøkelse
            ghost = Ghost(random.randint(space, WIDTH-space-w), random.randint(0, HEIGHT-w), LIGHTBLUE)
    # Tegner spøkelsene
    for g in ghosts:
        if coll_det(g):
            run = False
        g.draw()
        g.move()
    # Sjekker kollisjon med hindring
    if not human.pre_move():
        human.move()
    # Tegner mennesket
    human.draw()

    # Viser poeng
    display_text(f"Points: {points}", WHITE, BLACK, WIDTH/2, 20, 20)
    
    pg.display.flip()
    
# Viser at spillet er over samt poeng
display_text(f"You saved {points} sheep", WHITE, BLACK, WIDTH/2, HEIGHT/2+40, 20)
display_text(f"GAME OVER", WHITE, BLACK, WIDTH/2, HEIGHT/2, 50)
pg.display.flip()
# Avslutter vinduet
pg.quit()
# sys.exit()