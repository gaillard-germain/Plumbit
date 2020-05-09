#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: MIT

"""Importation des modules"""
import sys
import pygame
from random import randint
import json

def weighted(weighted_list):
    #Merci a Simon <Relic> GAILLARD pour cette fonction.
    '''return an item randomly from dict based on is weight
    (higher weights tend to be chosen more often)
    dict must be of the form : {'a': 10, 'b':4, 'c': 1}'''
    length = sum(weighted_list.values())
    index = randint(1,length)
    x = 0
    for key in weighted_list:
        x += weighted_list[key]
        if index <= x:
            return key

def rotate(pipe):
    """Fait tourner le tuyau (anti-horaire)"""
    coef = randint(0, 4)
    for i in range(coef):
        pipe.apertures.append(pipe.apertures.pop(0))
        pipe.image = pygame.transform.rotate(pipe.image, 90)
        if pipe.image_2:
            pipe.image_2 = pygame.transform.rotate(pipe.image_2, 90)
    return pipe

def open_to(pipe):
    """Pointe les coordonnees vers lesquels le tuyau est ouvert"""
    for index, aperture in enumerate(pipe.apertures):
        if aperture:
            if index == 0:
                yield ((pipe.rect.left - 60), pipe.rect.top)
            if index == 1:
                yield (pipe.rect.left, (pipe.rect.top - 60))
            if index == 2:
                yield (pipe.rect.right, pipe.rect.top)
            if index == 3:
                yield (pipe.rect.left, pipe.rect.bottom)

def pipe_dispenser():
    """Retourne un tuyau en fonction de sa 'rareté' """
    stock = {('images/cross.png', (1, 1, 1, 1)) : 10,
             ('images/regular_1.png', (0, 1, 0, 1)) : 50,
             ('images/regular_2.png', (0, 1, 1, 0)) : 40}
    return Pipe(weighted(stock))

def fill_box(box):
    """initialise la pioche"""
    box = []
    for i in range(4):
        pipe = pipe_dispenser()
        pipe = rotate(pipe)
        box.append(pipe)
    return box

def pick_up(box):
    """Pioche le tuyau courant et replace un autre en bout de pile"""
    pipe = box.pop(0)
    new = pipe_dispenser()
    new = rotate(new)
    box.append(new)
    return pipe

def cursor_pos(cursor, coords, area):
    """Maitien le curseur dans une zone definie"""
    cursor.topleft = (coords[0]-coords[0]%60, coords[1]-coords[1]%60)
    if cursor.left < area.left:
        cursor.left = area.left
    elif cursor.right > area.right:
        cursor.right = area.right
    if cursor.top < area.top:
        cursor.top = area.top
    elif cursor.bottom > area.bottom:
        cursor.bottom = area.bottom
    return cursor.topleft

def add(circuit, current):
    """Ajoute le tuyau courant au circuit"""
    for pipe in circuit:
        if pipe.rect.topleft == current.rect.topleft:
            circuit.remove(pipe)
    circuit.append(current)
    return circuit

def check(circuit, previous, path):
    """Retourne le bon tuyau"""
    eligibles = []
    elected = None
    for pipe in circuit:
        if (pipe.rect.topleft in list(open_to(previous)) and
        previous.rect.topleft in list(open_to(pipe))):
            eligibles.append(pipe)
    for pipe in eligibles:
        if previous.name == 'regular':
            elected = pipe
        elif previous.name == 'cross':
            if pipe.rect.topleft == (previous.rect.left + path[0],
                                     previous.rect.top + path[1]):
                elected = pipe
    return elected

def clog(path, apertures):
    """Bouche l'ouverture par laquelle le liquide est passé"""
    if path[0] < 0:
        apertures[2] = 0
    elif path[0] > 0:
        apertures[0] = 0
    if path[1] < 0:
        apertures[3] = 0
    elif path[1] > 0:
        apertures[1] = 0
    return apertures

def place_block(valve_1, valve_2, locked):
    """Empeche un block de se placer devant l'entree ou la sortie"""
    pos = (randint(0, 17) * 60,randint(0, 12) * 60)
    if pos in list(open_to(valve_1)) or pos in list(open_to(valve_2)):
        pos = place_block(valve_1, valve_2, locked)
    elif pos in locked:
        pos = place_block(valve_1, valve_2, locked)
    return pos

def load_json(data_file):
    with open(data_file) as data:
        return json.load(data)

def new_record(score, topten):
    """Verifie si le score peu entrer dans le top ten"""
    for index, player in enumerate(topten):
        if score > player["score"]:
            return index
    return None

def update_json(data_file, topten, index, winner, score):
    """met a jour le fichier json"""
    topten.insert(index, dict(name = winner, score = score))
    if len(topten) > 10:
        del topten[-1]
    with open(data_file, 'w') as file:
        json.dump(topten, file, indent = 4)
    return 0

def font_size(size):
    """Change la taille de la police principale"""
    return pygame.font.Font('fonts/Amatic-Bold.ttf', size)

class Pipe(object):
    """Un tuyau"""
    def __init__(self, ref):
        self.image = pygame.image.load(ref[0])
        self.image_2 = None
        self.apertures = list(ref[1])
        self.points = 100
        self.rect = self.image.get_rect()
        self.name = 'regular'
        if sum(self.apertures) == 4:
            self.name = 'cross'

class Plumbit(object):
    """Plumbit"""
    def __init__(self, score):
        pygame.init()
        pygame.display.set_caption("Plumb'it")
        self.topten = load_json('topten.json')
        self.layer1 = pygame.Surface((1080, 780), 32)
        self.layer2 = pygame.Surface((120, 780), 32)
        self.layer3 = pygame.Surface((1080, 780), pygame.SRCALPHA, 32)
        self.circuit = []
        self.locked = []
        self.box = []
        self.valve = Pipe(('images/valve_1.png', [0, 0, 1, 0]))
        self.valve.image_2 = pygame.image.load('images/valve_1a.png')
        self.end = Pipe(('images/valve_2.png', [0, 0, 1, 0]))
        self.liquid_image = pygame.image.load('images/liquid.png')
        self.liquid = self.liquid_image.get_rect()

        self.valve.rect.topleft = (randint(1, 7) * 60,
                              randint(1, 11) * 60)
        self.end.rect.topleft = (randint(10, 16) * 60,
                                 randint(1, 11) * 60)
        self.valve = rotate(self.valve)
        self.end = rotate(self.end)
        self.circuit.append(self.valve)
        self.circuit.append(self.end)
        self.locked.append(self.valve.rect.topleft)
        self.locked.append(self.end.rect.topleft)
        for i in range(randint(0, 4)):
            block = Pipe(('images/block.png', [0, 0, 0, 0]))
            block.rect.topleft = place_block(self.valve, self.end, self.locked)
            self.circuit.append(block)
            self.locked.append(block.rect.topleft)
        self.box = fill_box(self.box)
        self.previous = self.valve
        self.liquid.topleft = self.valve.rect.topleft
        self.countdown = 60
        self.score = score
        self.message = ''

    def main(self):
        screen = pygame.display.set_mode((1230, 800))
        COUNTDOWN = pygame.USEREVENT +1
        FLOOD = pygame.USEREVENT +2
        ANIM1 = pygame.USEREVENT +3
        ANIM2 = pygame.USEREVENT +4
        board = pygame.image.load('images/board.png')
        dashboard = pygame.image.load('images/panel.png')
        arrow = pygame.image.load('images/arrow.png')
        pointer_image = pygame.image.load('images/pointer.png')
        locked_image = pygame.image.load('images/locked.png')
        cursor_image = pointer_image
        cursor = cursor_image.get_rect()
        arrow_x = 5
        path = (0, 0)

        pygame.time.set_timer(ANIM1, 500)
        pygame.time.set_timer(ANIM2, 30)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEMOTION:
                    cursor.topleft = cursor_pos(cursor, pygame.mouse.get_pos(),
                                                self.layer1.get_rect())
                    if cursor.topleft in self.locked:
                        cursor_image = locked_image
                    else:
                        cursor_image = pointer_image
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.countdown == 60:
                            pygame.time.set_timer(COUNTDOWN, 1000)
                        if cursor.topleft not in self.locked:
                            pipe = pick_up(self.box)
                            pipe.rect.topleft = cursor.topleft
                            self.circuit = add(self.circuit, pipe)
                            self.score -= 50
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.time.set_timer(COUNTDOWN, 0)
                        pygame.time.set_timer(FLOOD, 20)
                elif event.type == ANIM1:
                    self.valve.image, self.valve.image_2 = (self.valve.image_2,
                                                            self.valve.image)
                elif event.type == ANIM2:
                    arrow_x += 1
                    if arrow_x > 20:
                        arrow_x = 5
                elif event.type == COUNTDOWN:
                    self.countdown -= 1
                    if self.countdown == 0:
                        pygame.time.set_timer(COUNTDOWN, 0)
                        pygame.time.set_timer(FLOOD, 40)
                elif event.type == FLOOD:
                    pipe = check(self.circuit, self.previous, path)
                    if pipe:
                        path = (pipe.rect.left - self.previous.rect.left,
                                pipe.rect.top - self.previous.rect.top)
                        self.liquid = self.liquid.move(path[0]/60, path[1]/60)
                        if self.liquid.topleft == self.end.rect.topleft:
                            pygame.time.set_timer(FLOOD, 0)
                            self.message = 'YOU WIN'
                        elif self.liquid.topleft == pipe.rect.topleft:
                            pipe.apertures = clog(path, pipe.apertures)
                            self.locked.append(pipe.rect.topleft)
                            self.score += 200
                            self.previous = pipe
                    else:
                        pygame.time.set_timer(FLOOD, 0)
                        self.message = 'YOU LOOSE'

            screen.blit(self.layer1, (10, 10))
            screen.blit(self.layer2, (1100, 10))
            screen.blit(self.layer3, (10, 10))

            self.layer1.blit(board, (0, 0))
            for pipe in self.circuit:
                self.layer1.blit(pipe.image, pipe.rect.topleft)
            self.layer1.blit(cursor_image, cursor.topleft)

            self.layer2.blit(dashboard, (0, 0))
            score_txt = font_size(40).render(str(self.score), True, (83, 162, 162))
            self.layer2.blit(score_txt, (30, 15))
            self.layer2.blit(arrow, (arrow_x, 430))
            y = 430
            for pipe in self.box:
                self.layer2.blit(pipe.image, (30, y))
                y -= 75
            countdown_txt = font_size(40).render(str(self.countdown), True,
                                        (70, 170, 60))
            self.layer2.blit(countdown_txt, (50, 690))

            self.layer3.blit(self.liquid_image, self.liquid.topleft)

            pygame.display.update()

            if self.message:
                """Fin de partie"""
                message_txt = font_size(72).render(self.message, True, (165, 80, 80))
                message2_txt = font_size(40).render('Press ENTER to continue', True,
                                            (165, 80, 80))
                self.layer3.blit(message_txt, (500, 50))
                self.layer3.blit(message2_txt, (460, 650))
                screen.blit(self.layer3, (10, 10))
                pygame.display.update()
                pygame.event.clear()
                while True:
                    event = pygame.event.wait()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if self.message == 'YOU WIN':
                                self.__init__(self.score)
                                break
                            elif self.message == 'YOU LOOSE':
                                rank = new_record(self.score, self.topten)
                                if rank != None:
                                    self.entry(rank)
                                else:
                                    self.__init__(0)
                                    self.menu()
                                    break

        return 0

    def menu(self):
        screen = pygame.display.set_mode((600, 900))
        title = font_size(72).render("PLUMB'IT", True, (170, 60, 60))
        screen.blit(title, (210, 50))
        y = 150
        for player in self.topten:
            name = font_size(40).render(player["name"], True, (50, 162, 162))
            score = font_size(40).render(str(player["score"]), True, (50, 162, 162))
            screen.blit(name, (150, y))
            screen.blit(score, (370, y))
            y += 50
        message_txt = font_size(32).render('Press ENTER to play', True, (170, 60, 60))
        screen.blit(message_txt, (220, 800))
        pygame.display.update()
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.main()
                    break
        return 0

    def entry(self, rank):
        screen = pygame.display.set_mode((640, 240))
        name = 'Enter your name'
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        if len(name)>0:
                            name = name[:-1]
                    elif event.key == pygame.K_RETURN:
                        update_json('topten.json', self.topten, rank, name, self.score)
                        self.__init__(0)
                        self.menu()
                        break
                    else:
                        name += event.unicode
            txt = font_size(40).render(name, True, (60, 170, 170))
            message = font_size(48).render((str(self.score) + ' is a new record !'),
                                           True, (70, 150, 150))
            screen.fill((0, 0, 0))
            screen.blit(message, (20, 20))
            screen.blit(txt, (50, 100))
            pygame.display.update()
        return 0

if __name__ == '__main__':
    Plumbit(0).menu()
