import pygame
from random import randint
from factory import Factory


class Circuit:
    def __init__(self):
        self.factory = Factory()
        self.circuit = []
        self.box = []
        self.score = 0
        self.lvl = 1

        self.liquid_image = pygame.image.load('images/liquid.png')
        self.liquid = self.liquid_image.get_rect()

    def reset(self):
        """ Reset score and level """
        self.score = 0
        self.lvl = 1

    def set_up(self):
        """ Set_up the circuit """
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

    def drop_and_pickup(self, pos):
        """ Place the current pipe and replace another in the pile """

        pipe = self.box.pop(0)
        pipe.rect.topleft = pos
        self.add(pipe)
        self.box.append(self.factory.get_pipe())
        self.score -= int(pipe.value / 2)

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
                self.score += self.end.value
                self.lvl += 1
                return 'YOU WIN'

            elif self.liquid.topleft == pipe.rect.topleft:
                pipe.clog(self.path)
                self.previous = pipe
                self.score += pipe.value
                return False

        else:
            return 'YOU LOOSE'

    def draw_box(self, surface):
        """ Blit the pipes in the pipes box """
        for i, pipe in enumerate(self.box):
            surface.blit(pipe.image, (150, 470 + i * 70))

    def draw_pipes(self, surface):
        """ Blit all the pipes in the circuit """
        for pipe in self.circuit:
            surface.blit(pipe.image, pipe.rect.topleft)

    def draw_liquid(self, surface):
        """ Blit the liquid """
        surface.blit(self.liquid_image, self.liquid.topleft)
