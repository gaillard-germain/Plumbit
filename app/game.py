import pygame
from random import randint

from factory import Factory
from sound import Sound
from tools import display_txt
from sprites.cursor import Cursor
from sprites.button import Button
from sprites.liquid import Liquid
from sprites.bubble import Bubble
from sprites.arrow import Arrow


class Game:
    def __init__(self, screen):
        self.tile_size = 64
        self.tile_x = 17
        self.tile_y = 12
        self.screen = screen
        self.factory = Factory()
        self.sound = Sound()

        self.flood_btn = Button('FLOOD', (140, 50), self.flood_now)
        self.giveup_btn = Button('GIVE-UP', (140, 150), self.give_up)
        self.continue_btn = Button('CONTINUE', (140, 50), self.next_step)

        self.COUNTDOWN = pygame.USEREVENT + 1
        self.FLOOD = pygame.USEREVENT + 2
        self.ANIM = pygame.USEREVENT + 3

        self.circuit = {}

        for y in range(self.tile_y):
            for x in range(self.tile_x):
                self.circuit[(x*self.tile_size, y*self.tile_size)] = None

        self.box = []
        self.score = 0
        self.lvl = 0
        self.time = 60
        self.state = 'WAITING'

        self.dashboard_left = pygame.image.load('./images/dashboard_left.png')
        self.dashboard_right = pygame.image.load(
            './images/dashboard_right.png')

        self.layer1 = pygame.Surface(
            (self.tile_size*self.tile_x, self.tile_size*self.tile_y),
            pygame.SRCALPHA,
            32
        )
        self.layer2 = pygame.Surface(
            (self.tile_size*self.tile_x, self.tile_size*self.tile_y),
            pygame.SRCALPHA,
            32
        )

        self.board = self.layer1.get_rect()

        self.board.topleft = (0, 0)

        self.board_offset = (
            (self.screen.get_width() - self.board.width)/2,
            (self.screen.get_height() - self.board.height)/2
        )
        self.cursor = Cursor(self.board_offset)
        self.bubble = Bubble(self.tile_size)
        self.arrow = Arrow()

    def reset(self):
        """ Reset score, level and time """
        self.score = 0
        self.lvl = 0
        self.time = 60
        self.set_up()

    def clear_circuit(self):
        for pos in self.circuit.keys():
            self.circuit[pos] = None

    def set_up(self):
        """ Set_up the circuit """

        self.layer2.fill((255, 255, 255, 0))

        self.clear_circuit()

        self.fill_box()

        for i in range(randint(self.lvl, self.lvl+1)):
            block = self.factory.get_extra('block')
            block.randomize_image()
            self.strew(block)

        self.valve = self.factory.get_extra('valve')
        self.valve.rotate()
        self.strew(self.valve, margin=1)

        self.end = self.factory.get_extra('end')
        self.end.rotate()
        self.strew(self.end, margin=1)

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

    def is_free(self, pipe):
        if self.circuit[pipe.rect.topleft]:
            return False
        else:
            for pos in pipe.open_to():
                if self.circuit[pos]:
                    return False
        return True

    def strew(self, pipe, margin=0):
        """ Randomly place pipe in the circuit """

        while True:
            pipe.rect.topleft = (
                randint(0+margin, self.tile_x-(1+margin)) * pipe.rect.width,
                randint(0+margin, self.tile_y-(1+margin)) * pipe.rect.height
            )

            if self.is_free(pipe):
                break

        self.circuit[pipe.rect.topleft] = pipe

    def fill_box(self):
        """ Refill the pipe's box """

        if self.box:
            self.box.clear()

        for i in range(5):
            pipe = self.factory.get_pipe()
            pipe.rect.topleft = (250, 460 + i * 80)
            self.box.append(pipe)

    def pickup(self):
        picked = self.box.pop(0)
        self.box.append(self.factory.get_pipe())
        for i, pipe in enumerate(self.box):
            pipe.rect.topleft = (250, 460 + i * 80)

        return picked

    def drop_and_pickup(self, pos):
        """ Place the current pipe and replace another in the pile """

        self.sound.put.play()
        pipe = self.pickup()
        pipe.rect.topleft = pos
        self.circuit[pipe.rect.topleft] = pipe

        self.update_gain(pipe.rect.topleft, pipe.cost)

    def get_locked(self):
        """ Get the list of the locked pipes """

        for pipe in self.circuit.values():
            if pipe and pipe.locked:
                yield pipe.rect.topleft

    def is_locked(self, pos):
        """ Checks if the position is locked """

        if pos in self.get_locked():
            return True
        else:
            return False

    def process(self):
        self.flood_btn.process()
        self.giveup_btn.process()
        self.continue_btn.process()

        self.cursor.process(self.is_locked)
        self.bubble.process()

        self.draw()

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
        self.valve.anim()
        self.countdown -= 1
        if self.countdown <= 0:
            pygame.time.set_timer(self.COUNTDOWN, 0)
            pygame.time.set_timer(self.FLOOD, 50)
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
        self.bubble.update(pos, value)

    def draw(self):

        self.screen.fill((66, 63, 56))
        self.layer1.fill((96, 93, 86))

        for pipe in self.circuit.values():
            if pipe:
                pipe.draw(self.layer1)

        self.bubble.draw(self.layer1)
        self.cursor.draw(self.layer1)
        self.liquid.draw(self.layer2)

        self.screen.blit(self.layer1, self.board_offset)
        self.screen.blit(self.layer2, self.board_offset)

        self.screen.blit(self.dashboard_left, (0, 0))
        self.screen.blit(
            self.dashboard_right,
            (self.screen.get_width() - self.dashboard_right.get_width(), 0)
        )

        display_txt(self.score, 40, (83, 162, 162), self.screen,
                    1678, 177)
        display_txt(self.countdown, 40, (70, 170, 60), self.screen,
                    1680, 900)

        self.arrow.draw(self.screen)

        for pipe in self.box:
            pipe.draw(self.screen)

        if self.state == 'WIN' or self.state == 'LOOSE':
            display_txt('YOU {}'.format(self.state), 72, (194, 69, 26),
                        self.screen, None, 60)
            txt = 'Click CONTINUE Button'
            display_txt(txt, 40, (194, 69, 26), self.screen, None,
                        self.screen.get_height()-60)
            self.continue_btn.draw(self.screen)

        else:
            self.flood_btn.draw(self.screen)
            self.giveup_btn.draw(self.screen)

    def anim(self):
        self.bubble.anim()
        self.arrow.anim()

    # ## Buttons callbacks ## #

    def flood_now(self):
        """ Flood Button callback """

        self.sound.sub.play()
        pygame.time.set_timer(self.COUNTDOWN, 0)
        pygame.time.set_timer(self.FLOOD, 20)

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
