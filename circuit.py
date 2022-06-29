import pygame
from random import randint
from pipe import Pipe


class Circuit:
    def __init__(self):
        self.circuit = []
        self.box = []

        self.valve = Pipe(
            {
                'image': 'images/valve_1.png',
                'image2': 'images/valve_1a.png',
                'apertures': [0, 0, 1, 0],
                'name': 'regular'
                }
        )
        self.end = Pipe(
            {
                'image': 'images/valve_2.png',
                'image2': None,
                'apertures': [0, 0, 1, 0],
                'name': 'end'
                }
        )
        self.liquid_image = pygame.image.load('images/liquid.png')
        self.liquid = self.liquid_image.get_rect()
        self.previous = self.valve

        self.valve.rect.topleft = (randint(1, 5) * 60, randint(1, 9) * 60)
        self.end.rect.topleft = (randint(9, 13) * 60, randint(1, 9) * 60)
        self.valve = self.valve.rotate()
        self.end = self.end.rotate()
        self.circuit.append(self.valve)
        self.circuit.append(self.end)
        self.valve.lock()
        self.end.lock()
        for i in range(randint(0, 5)):
            block = Pipe(
                {
                    'image': 'images/block.png',
                    'image2': None,
                    'apertures': [0, 0, 0, 0],
                    'name': 'block'
                    }
            )
            self.place_block(block)

        self.fill_box()
        self.previous = self.valve
        self.liquid.topleft = self.valve.rect.topleft
        self.path = (0, 0)

    def place_block(self, block):
        """Empeche un block de se placer devant l'entree ou la sortie"""

        pos = (randint(0, 14) * 60, randint(0, 9) * 60)
        if (pos in self.valve.open_to() or pos in self.end.open_to()):
            pos = self.place_block(block)
        elif self.is_locked(pos):
            pos = self.place_block(block)

        block.rect.topleft = pos

        self.circuit.append(block)
        block.lock()

    def fill_box(self):
        """initialise la pioche"""

        self.box = []

        for i in range(4):
            pipe = Pipe.create()
            pipe = pipe.rotate()
            self.box.append(pipe)

    def drop_and_pickup(self, pos):
        """Pioche le tuyau courant et replace un autre en bout de pile"""
        pipe = self.box.pop(0)
        pipe.rect.topleft = pos
        new = Pipe.create()
        new = new.rotate()
        self.box.append(new)
        self.add(pipe)

        return pipe.rect.topleft

    def add(self, current):
        """Ajoute le tuyau courant au circuit"""

        for pipe in self.circuit:
            if pipe.rect.topleft == current.rect.topleft:
                self.circuit.remove(pipe)

        self.circuit.append(current)

    def check(self):
        """Retourne le bon tuyau"""
        eligibles = []
        elected = None
        for pipe in self.circuit:
            if (pipe.rect.topleft in list(self.previous.open_to())
                    and self.previous.rect.topleft in list(pipe.open_to())):
                eligibles.append(pipe)
        for pipe in eligibles:
            if self.previous.name == 'regular':
                elected = pipe
            elif self.previous.name == 'cross':
                if pipe.rect.topleft == (self.previous.rect.left+self.path[0],
                                         self.previous.rect.top+self.path[1]):
                    elected = pipe
        return elected

    def anim_valve(self):
        self.valve.image, self.valve.image_2 = (self.valve.image_2,
                                                self.valve.image)

    def get_locked(self):
        for pipe in self.circuit:
            if pipe.locked:
                yield pipe.rect.topleft

    def is_locked(self, pos):
        if pos in self.get_locked():
            return True
        else:
            return False

    def flood(self):
        pipe = self.check()
        if pipe:
            self.path = (pipe.rect.left - self.previous.rect.left,
                         pipe.rect.top - self.previous.rect.top)
            self.liquid = self.liquid.move(int(self.path[0]/60),
                                           int(self.path[1]/60))
            if self.liquid.topleft == self.end.rect.topleft:
                return 'YOU WIN'

            elif self.liquid.topleft == pipe.rect.topleft:
                pipe.clog(self.path)
                self.previous = pipe
                return 'PASS'

        else:
            return 'YOU LOOSE'

    def draw_box(self, surface):
        for i, pipe in enumerate(self.box):
            surface.blit(pipe.image, (150, 470 + i * 70))

    def draw_pipes(self, surface):
        for pipe in self.circuit:
            surface.blit(pipe.image, pipe.rect.topleft)

    def draw_liquid(self, surface):
        surface.blit(self.liquid_image, self.liquid.topleft)
