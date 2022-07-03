import pygame
from random import randint

from factory import Factory
from cursor import Cursor
from tools import display_txt


class Game:
    def __init__(self):
        self.factory = Factory()
        self.cursor = Cursor()
        self.circuit = []
        self.box = []
        self.score = 0
        self.lvl = 1
        self.state = 'WAITING'

        self.liquid_image = pygame.image.load('images/liquid.png')
        self.dashboard = pygame.image.load('images/dashboard.png')
        self.back = pygame.image.load('images/dashboard_back.png')
        self.arrow_image = pygame.image.load('images/arrow.png')

        self.layer1 = pygame.Surface((900, 660), 32)
        self.layer2 = pygame.Surface((900, 660), pygame.SRCALPHA, 32)
        self.layer3 = pygame.Surface((134, 682), pygame.SRCALPHA, 32)

        self.liquid = self.liquid_image.get_rect()
        self.board = self.layer1.get_rect()
        self.arrow = self.arrow_image.get_rect()

        self.board.topleft = (250, 120)
        self.arrow.topleft = (120, 485)

    def reset(self):
        """ Reset score and level """
        self.score = 0
        self.lvl = 0
        self.countdown = 60
        self.state = 'WAITING'

    def set_up(self):
        """ Set_up the circuit """

        self.layer2.fill((255, 255, 255, 0))

        if self.circuit:
            self.circuit.clear()

        self.fill_box()

        self.valve = self.factory.get_extra('valve').rotate()
        self.end = self.factory.get_extra('end').rotate()

        self.valve.rect.topleft = (randint(1, 5) * 60, randint(1, 9) * 60)
        self.end.rect.topleft = (randint(9, 13) * 60, randint(1, 9) * 60)

        self.circuit.append(self.valve)
        self.circuit.append(self.end)

        for i in range(randint(int(self.lvl / 2), self.lvl)):
            self.place_block(self.factory.get_extra('block'))

        self.previous = self.valve
        self.liquid.topleft = self.valve.rect.topleft
        self.path = (0, 0)
        self.countdown = 60 - self.lvl
        self.state = 'WAITING'

    def process(self):
        self.cursor.process(self.board, self.is_locked)

    def place_block(self, block):
        """ Prevents a block from being placed in front of
            the entrance or the exit """

        pos = (randint(0, 14) * 60, randint(0, 9) * 60)
        if (pos in self.valve.open_to()
                or pos in self.end.open_to()
                or self.is_locked(pos)):
            return
        else:
            block.rect.topleft = pos
            self.circuit.append(block)

    def fill_box(self):
        """ Refill the pipe's box """

        if self.box:
            self.box.clear()

        for _ in range(4):
            self.box.append(self.factory.get_pipe())

    def drop_and_pickup(self):
        """ Place the current pipe and replace another in the pile """

        pos = self.cursor.rect.topleft

        if not self.is_locked(pos):
            pipe = self.box.pop(0)
            pipe.rect.topleft = pos
            self.add(pipe)
            self.box.append(self.factory.get_pipe())
            self.score -= int(pipe.value / 2)

            return True

    def add(self, current):
        """ Adds the current pipe to the circuit """

        for pipe in self.circuit:
            if pipe.rect.topleft == current.rect.topleft:
                self.circuit.remove(pipe)

        self.circuit.append(current)

    def check(self):
        """ Returns the next floodable pipe """
        eligibles = []
        elected = None
        for pipe in self.circuit:
            if (pipe.rect.topleft in self.previous.open_to()
                    and self.previous.rect.topleft in pipe.open_to()):
                eligibles.append(pipe)
        for pipe in eligibles:
            if self.previous.name == 'regular':
                elected = pipe
            elif self.previous.name == 'cross':
                if pipe.rect.topleft == (self.previous.rect.left+self.path[0],
                                         self.previous.rect.top+self.path[1]):
                    elected = pipe
        return elected

    def get_locked(self):
        """ Get the list of the locked pipes """

        for pipe in self.circuit:
            if pipe.locked:
                yield pipe.rect.topleft

    def is_locked(self, pos):
        """ Checks if the position is locked """

        if pos in self.get_locked():
            return True
        else:
            return False

    def flood(self):
        """ Floods the circuit """

        pipe = self.check()
        if pipe:
            self.path = (pipe.rect.left - self.previous.rect.left,
                         pipe.rect.top - self.previous.rect.top)
            self.liquid = self.liquid.move(int(self.path[0]/60),
                                           int(self.path[1]/60))
            if self.liquid.topleft == self.end.rect.topleft:
                self.score += self.end.value + self.countdown * 10
                self.lvl += 1
                self.state = 'WIN'

            elif self.liquid.topleft == pipe.rect.topleft:
                pipe.clog(self.path)
                self.previous = pipe
                self.score += pipe.value

        else:
            self.state = 'LOOSE'

    def draw(self, surface):
        surface.blit(self.layer1, self.board.topleft)
        surface.blit(self.layer2, self.board.topleft)
        surface.blit(self.dashboard, (0, 0))
        surface.blit(self.layer3, (1167, 115))
        surface.blit(self.arrow_image, self.arrow.topleft)

        for i, pipe in enumerate(self.box):
            surface.blit(pipe.image, (150, 470 + i * 70))

        self.layer1.fill((96, 93, 86))

        for pipe in self.circuit:
            self.layer1.blit(pipe.image, pipe.rect.topleft)

        self.cursor.draw(self.layer1)

        self.layer2.blit(self.liquid_image, self.liquid.topleft)

        self.layer3.blit(self.back, (0, 0))

        display_txt(self.score, 40, (83, 162, 162), self.layer3,
                    'center', 5)
        display_txt(self.countdown, 40, (70, 170, 60), self.layer3,
                    'center', 625)
