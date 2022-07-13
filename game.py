import pygame
from random import randint

from factory import Factory
from cursor import Cursor
from button import Button
from liquid import Liquid
from sound import Sound
from tools import display_txt, center


class Game:
    def __init__(self):
        self.factory = Factory()
        self.cursor = Cursor()
        self.sound = Sound()

        self.flood_btn = Button('FLOOD', (20, 50), self.flood_now)
        self.giveup_btn = Button('GIVE-UP', (20, 150), self.give_up)
        self.continue_btn = Button('CONTINUE', (20, 250), self.next_step)

        self.COUNTDOWN = pygame.USEREVENT + 1
        self.FLOOD = pygame.USEREVENT + 2
        self.ANIM = pygame.USEREVENT + 3

        self.circuit = []
        self.box = []
        self.score = 0
        self.lvl = 0
        self.time = 60
        self.state = 'WAITING'

        self.dashboard = pygame.image.load('images/dashboard.png')
        self.arrow_image = pygame.image.load('images/arrow.png')

        self.layer1 = pygame.Surface((900, 660), pygame.SRCALPHA, 32)
        self.layer2 = pygame.Surface((900, 660), pygame.SRCALPHA, 32)
        self.layer3 = pygame.Surface((134, 900), pygame.SRCALPHA, 32)
        self.layer4 = pygame.Surface((60, 60), pygame.SRCALPHA, 32)

        self.board = self.layer1.get_rect()
        self.arrow = self.arrow_image.get_rect()
        self.pipe_score = self.layer4.get_rect()

        self.board.topleft = (0, 0)
        self.arrow.topleft = (120, 485)

    def reset(self):
        """ Reset score, level and time """
        self.score = 0
        self.lvl = 0
        self.time = 60
        self.set_up()

    def set_up(self):
        """ Set_up the circuit """

        self.layer2.fill((255, 255, 255, 0))

        if self.circuit:
            self.circuit.clear()

        self.fill_box()

        self.valve = self.factory.get_extra('valve').rotate()
        self.end = self.factory.get_extra('end').rotate()

        self.valve.rect.topleft = (
            randint(1, 5) * self.valve.rect.width,
            randint(1, 9) * self.valve.rect.height
        )
        self.end.rect.topleft = (
            randint(9, 13) * self.end.rect.width,
            randint(1, 9) * self.end.rect.height
        )

        self.circuit.append(self.valve)
        self.circuit.append(self.end)
        self.place_block()

        self.lvl += 1
        self.set_time()
        self.countdown = self.time
        self.state = 'WAITING'

        self.liquid = Liquid(self.valve, self.end, self.update_gain)

        pygame.time.set_timer(self.ANIM, 15)

        pygame.mixer.music.play(loops=-1)

    def set_time(self):
        if not self.lvl % 5 and self.time > 5:
            self.time -= 5

    def process(self):
        self.flood_btn.process()
        self.giveup_btn.process()
        self.continue_btn.process()

        self.cursor.process(self.board, self.is_locked)

        if self.pipe_score.top <= -20:
            self.layer4.fill((255, 255, 255, 0))

    def place_block(self):
        """ Place several blocks in the circuit """

        for i in range(randint(self.lvl, self.lvl+1)):
            block = self.factory.get_extra('block')

            pos = (
                randint(0, 14) * block.rect.width,
                randint(0, 9) * block.rect.height
            )
            if (pos in self.valve.open_to()
                    or pos in self.end.open_to()
                    or self.is_locked(pos)):
                continue
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

        self.sound.put.play()
        pipe = self.box.pop(0)
        pipe.rect.topleft = pos
        self.add(pipe)
        self.box.append(self.factory.get_pipe())

        self.update_gain(pipe.rect.topleft, pipe.cost)

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

    def on_mouse_click(self):
        if self.state == 'LOOSE' or self.state == 'WIN':
            emit = self.continue_btn.click()

        else:
            pos = self.cursor.rect.topleft

            emit = self.flood_btn.click()
            emit = self.giveup_btn.click()

            if self.state == 'WAITING':
                self.state = 'RUNNING'
                pygame.time.set_timer(self.COUNTDOWN, 1000)

            if (self.board.contains(self.cursor.rect)
                    and not self.is_locked(pos)):
                self.drop_and_pickup(pos)

        return emit

    def tic(self):
        self.sound.tic.play()
        self.countdown -= 1
        self.valve.anim()
        if self.countdown <= 0:
            pygame.time.set_timer(self.COUNTDOWN, 0)
            pygame.time.set_timer(self.FLOOD, 30)
            self.sound.sub.play()

    def flood(self):
        """ Floods the circuit """

        state = self.liquid.flood(self.circuit, self.countdown)
        if state:
            self.state = state

        if self.state == 'WIN':
            pygame.time.set_timer(self.FLOOD, 0)
            pygame.mixer.music.stop()
            self.sound.win.play()

        elif self.state == 'LOOSE':
            pygame.time.set_timer(self.FLOOD, 0)
            pygame.mixer.music.stop()
            self.sound.loose.play()

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

        surface.blit(self.layer1, center(surface, self.layer1))
        surface.blit(self.layer2, center(surface, self.layer1))

        surface.blit(self.dashboard, center(surface, self.dashboard))
        surface.blit(self.layer3, (1167, 0))
        surface.blit(self.arrow_image, self.arrow.topleft)

        for i, pipe in enumerate(self.box):
            surface.blit(pipe.image, (150, 470 + i * 70))

        self.layer1.fill((96, 93, 86))
        self.layer3.fill((255, 255, 255, 0))

        for pipe in self.circuit:
            self.layer1.blit(pipe.image, pipe.rect.topleft)

        self.cursor.draw(self.layer1)
        self.liquid.draw(self.layer2)

        display_txt(self.score, 40, (83, 162, 162), self.layer3,
                    'center', 124)
        display_txt(self.countdown, 40, (70, 170, 60), self.layer3,
                    'center', 747)

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
            self.pipe_score.move_ip(0, -2)

        if self.arrow.left > 90:
            self.arrow.move_ip(-1, 0)
        else:
            self.arrow.left = 120

    # ## Buttons callbacks ## #

    def flood_now(self):
        """ Flood Button callback """

        self.sound.sub.play()
        pygame.time.set_timer(self.COUNTDOWN, 0)
        pygame.time.set_timer(self.FLOOD, 15)

    def give_up(self):
        """ Give-up Button callback """

        pygame.mixer.music.stop()
        pygame.time.set_timer(self.COUNTDOWN, 0)
        pygame.time.set_timer(self.FLOOD, 0)
        pygame.time.set_timer(self.ANIM, 0)

        return 'LOOSE'

    def next_step(self):
        """ Continue Button callback """

        if self.state == 'WIN':
            self.set_up()

        elif self.state == 'LOOSE':
            return self.give_up()
