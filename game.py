import pygame
from random import randint

from factory import Factory
from cursor import Cursor
from liquid import Liquid
from tools import display_txt


class Game:
    def __init__(self, flood_btn, giveup_btn, continue_btn):
        self.factory = Factory()
        self.cursor = Cursor()

        self.flood_btn = flood_btn
        self.giveup_btn = giveup_btn
        self.continue_btn = continue_btn

        self.circuit = []
        self.box = []
        self.score = 0
        self.lvl = 1
        self.state = 'WAITING'

        self.dashboard = pygame.image.load('images/dashboard.png')
        self.back = pygame.image.load('images/dashboard_back.png')
        self.arrow_image = pygame.image.load('images/arrow.png')

        self.layer1 = pygame.Surface((900, 660), 32)
        self.layer2 = pygame.Surface((900, 660), pygame.SRCALPHA, 32)
        self.layer3 = pygame.Surface((134, 682), pygame.SRCALPHA, 32)
        self.layer4 = pygame.Surface((60, 60), pygame.SRCALPHA, 32)

        self.board = self.layer1.get_rect()
        self.arrow = self.arrow_image.get_rect()
        self.pipe_score = self.layer4.get_rect()

        self.board.topleft = (250, 120)
        self.arrow.topleft = (120, 485)

    def reset(self):
        """ Reset score and level """
        self.score = 0
        self.lvl = 0
        self.countdown = 60
        self.set_up()

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

        self.countdown = 60 - self.lvl
        self.state = 'WAITING'

        self.liquid = Liquid(self.valve, self.end, self.update_gain)

        pygame.mixer.music.play(loops=-1)

    def process(self):
        self.flood_btn.process()
        self.giveup_btn.process()
        self.continue_btn.process()

        self.cursor.process(self.board, self.is_locked)

        if self.pipe_score.top <= -20:
            self.layer4.fill((255, 255, 255, 0))

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
            cost = - int(pipe.value / 2)
            pipe.rect.topleft = pos
            self.add(pipe)
            self.box.append(self.factory.get_pipe())

            self.update_gain(pipe.rect.topleft, cost)

            return True

    def add(self, current):
        """ Adds the current pipe to the circuit """

        for pipe in self.circuit:
            if pipe.rect.topleft == current.rect.topleft:
                self.circuit.remove(pipe)

        self.circuit.append(current)

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

        state = self.liquid.flood(self.circuit)
        if state:
            self.state = state

    def update_gain(self, pos, value):
        self.score += value
        self.pipe_score.topleft = pos
        self.layer4.fill((255, 255, 255, 0))
        if int(value) > 0:
            txt = '+{} $'.format(value)
            color = (70, 170, 60)
        else:
            txt = '{} $'.format(value)
            color = (194, 69, 26)

        display_txt(txt, 26, color, self.layer4)

    def draw(self, surface):
        surface.fill((66, 63, 56))

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
        self.liquid.draw(self.layer2)

        self.layer3.blit(self.back, (0, 0))

        display_txt(self.score, 40, (83, 162, 162), self.layer3,
                    'center', 8)
        display_txt(self.countdown, 40, (70, 170, 60), self.layer3,
                    'center', 632)

        surface.blit(self.flood_btn.image, self.flood_btn.rect.topleft)
        surface.blit(self.giveup_btn.image, self.giveup_btn.rect.topleft)

        self.layer1.blit(self.layer4, self.pipe_score.topleft)

        if self.state == 'WIN' or self.state == 'LOOSE':
            display_txt('YOU {}'.format(self.state), 72,
                        (194, 69, 26), surface, 'center', 20)
            txt = 'Click CONTINUE Button'
            display_txt(txt, 40, (194, 69, 26), surface,
                        'center', 800)
            surface.blit(self.continue_btn.image,
                         self.continue_btn.rect.topleft)

    def anim(self):
        if self.pipe_score.top >= -20:
            self.pipe_score = self.pipe_score.move(0, -2)

        if self.arrow.left > 90:
            self.arrow = self.arrow.move(-1, 0)
        else:
            self.arrow.left = 120
