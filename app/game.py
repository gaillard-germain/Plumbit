import pygame
from random import randint, choice

from factory import Factory
from sound import Sound
from sprites.cursor import Cursor
from sprites.button import Button
from sprites.liquid import Liquid
from sprites.arrow import Arrow
from sprites.stamp import Stamp


class Game:
    INFO = [
        'Countdown starts when you place the first pipe.',
        'The golden-cross doubles your gains but speeds up the liquid.',
        'The chance to have a golden-cross increases with the level.',
        'When the liquid crosses a cross it goes straight.',
        'Time decreases by 5 seconds every 5 levels.',
        'The Flood button starts the liquid immediately.',
        'The give-up button brings you back to the menu.',
        'You cannot replace a flooded pipe.',
        'The number of obstacles increases with the level.'
    ]

    def __init__(self, screen):
        self.tile_size = 64
        self.tile_x = 17
        self.tile_y = 12
        self.screen = screen
        self.factory = Factory()
        self.sound = Sound()
        self.music = True

        self.flood_btn = Button(['FLOOD'], (140, 50), self.flood_now)
        self.giveup_btn = Button(['GIVE-UP'], (140, 150), self.give_up)
        self.continue_btn = Button(['CONTINUE'], (140, 50), self.next_step)

        self.COUNTDOWN = pygame.USEREVENT + 1
        self.FLOOD = pygame.USEREVENT + 2
        self.ANIM = pygame.USEREVENT + 3

        self.circuit = {}

        for y in range(self.tile_y):
            for x in range(self.tile_x):
                self.circuit[(x*self.tile_size, y*self.tile_size)] = None

        self.box = []
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
        self.score = Stamp(0, 40, 'green', (1673, 177))

        self.message_top = Stamp('', 72, 'orange',
                                 (self.screen.get_width()/2, 100))
        self.message_bottom = Stamp('', 40, 'orange',
                                    (self.screen.get_width()/2,
                                     self.screen.get_height()-100))

        self.plop = Stamp('', 32)
        self.arrow = Arrow()

        self.valve = self.factory.get_extra('valve')
        self.end = self.factory.get_extra('end')

    def reset(self):
        """ Reset score, level and time """
        self.score.set_txt(0)
        self.lvl = 0
        self.time = 60

        pygame.time.set_timer(self.ANIM, 15)
        self.set_up()

    def set_up(self):
        """ Set_up the game """

        self.layer2.fill((255, 255, 255, 0))

        self.lvl += 1
        self.state = 'WAITING'

        self.message_top.set_txt('Level {}'.format(self.lvl))
        self.message_bottom.set_txt(
            'Info: {}'.format(choice(self.INFO)))

        self.fill_box()
        self.set_time()
        self.strew()

        self.liquid = Liquid(self.valve, self.end, self.circuit,
                             self.update_gain, self.FLOOD)

        self.countdown = Stamp(self.time, 40, 'light-blue', (1680, 900))

        if self.music:
            pygame.mixer.music.play(loops=-1)

    def set_time(self):
        """ Decrease time for each 5 lvl """

        if not self.lvl % 5 and self.time > 5:
            self.time -= 5

    def clear_circuit(self):
        """ Clear the circuit dict """

        for pos in self.circuit.keys():
            self.circuit[pos] = None

    def get_nexts(self, pos):
        """ Util method for generating a ghost path to the end """

        for i in (-self.tile_size, self.tile_size):
            x = (pos[0]+i, pos[1])
            if x in self.circuit.keys() and self.circuit[x] is None:
                yield x
            y = (pos[0], pos[1]+i)
            if y in self.circuit.keys() and self.circuit[y] is None:
                yield y

    def strew(self):
        """ Strew valve, end and several blocks on the game board """

        self.clear_circuit()

        pos = (randint(1, self.tile_x-2) * self.tile_size,
               randint(1, self.tile_y-2) * self.tile_size)

        self.circuit[pos] = '#'
        self.valve.rect.topleft = choice(list(self.get_nexts(pos)))
        self.circuit[self.valve.rect.topleft] = self.valve
        self.valve.align(pos)

        while True:
            nexts = list(self.get_nexts(pos))
            if nexts:
                prev = pos
                pos = choice(nexts)
                self.circuit[pos] = '#'
            else:
                break

        self.end.rect.topleft = pos
        self.circuit[pos] = self.end
        self.end.align(prev)

        for i in range(randint(self.lvl, self.lvl+1)):
            block = self.factory.get_extra('block')
            block.randomize_image()

            free = list(self.get_free())

            if free:
                block.rect.topleft = choice(free)
                self.circuit[block.rect.topleft] = block
            else:
                break

        if randint(0, 100) < self.lvl:
            golden = self.factory.get_extra('golden')
            golden.rect.topleft = (choice(list(self.get_path())))
            self.circuit[golden.rect.topleft] = golden

        for pos in self.get_path():
            self.circuit[pos] = None

    def get_path(self):
        """ Get the ghost path positions """

        for pos, pipe in self.circuit.items():
            if pipe == '#':
                yield pos

    def get_free(self):
        """ Get the list of free positions """

        for pos, pipe in self.circuit.items():
            if pipe is None:
                yield pos

    def fill_box(self):
        """ Refill the pipe's box """

        if self.box:
            self.box.clear()

        for i in range(5):
            pipe = self.factory.get_pipe()
            pipe.rect.topleft = (250, 460 + i * 80)
            self.box.append(pipe)

    def pickup(self):
        """ Pickup the first pipe in the box
            and add a new random one in the queue """

        picked = self.box.pop(0)
        self.box.append(self.factory.get_pipe())
        for i, pipe in enumerate(self.box):
            pipe.rect.topleft = (250, 460 + i * 80)

        return picked

    def drop_and_pickup(self, pos):
        """ Place the current pipe and replace another in the pile """

        if self.state == 'WAITING':
            self.state = 'RUNNING'
            pygame.time.set_timer(self.COUNTDOWN, 1000)
            self.message_bottom.set_txt('Incoming fluid...')

        self.sound.put.play()
        pipe = self.pickup()
        pipe.rect.topleft = pos
        self.circuit[pipe.rect.topleft] = pipe

        self.update_gain(pipe.rect.center, pipe.cost)

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
        """ Process buttons, cursor and drawing """

        self.flood_btn.process()
        self.giveup_btn.process()
        self.continue_btn.process()

        self.cursor.process(self.is_locked)

        self.draw()

    def on_mouse_click(self):
        """ Handle button click event """

        if self.state == 'LOOSE' or self.state == 'WIN':
            emit = self.continue_btn.click()

        else:
            pos = self.cursor.rect.topleft

            emit = self.flood_btn.click()
            emit = self.giveup_btn.click()

            if (self.board.contains(self.cursor.rect)
                    and not self.is_locked(pos)):
                self.drop_and_pickup(pos)

        return emit

    def tic(self):
        """ Decrease countdown every second, and start flooding at 0 """

        self.sound.tic.play()
        self.valve.anim()
        self.countdown.set_txt(int(self.countdown.txt) - 1)
        if int(self.countdown.txt) <= 0:
            pygame.time.set_timer(self.COUNTDOWN, 0)
            pygame.time.set_timer(self.FLOOD, 50)
            self.sound.sub.play()
            self.message_bottom.set_txt('HURRY !!!')

    def flood(self):
        """ Floods the circuit """

        state = self.liquid.flood(int(self.countdown.txt))
        if state:
            self.state = state

        if self.state == 'WIN':
            pygame.time.set_timer(self.FLOOD, 0)
            pygame.mixer.music.stop()
            self.sound.win.play()
            self.message_top.set_txt('YOU WIN')
            self.message_bottom.set_txt('Click CONTINUE button')

        elif self.state == 'LOOSE':
            pygame.time.set_timer(self.COUNTDOWN, 0)
            pygame.time.set_timer(self.FLOOD, 0)
            pygame.mixer.music.stop()
            self.sound.loose.play()
            self.message_top.set_txt('YOU LOOSE')
            self.message_bottom.set_txt('Click CONTINUE button')

    def update_gain(self, pos, value):
        """ Modify score every time a pipe is flooded or placed """

        self.score.set_txt(int(self.score.txt) + value)

        if int(value) > 0:
            txt = '+{} $'.format(value)
            color = 'green'
        else:
            txt = '{} $'.format(value)
            color = 'red'

        self.plop.set_txt(txt, color, pos)

    def switch_music(self):
        self.music = not self.music

    def draw(self):
        """ Draw every game things on screen """

        self.screen.fill((66, 63, 56))
        self.layer1.fill((96, 93, 86))

        for pipe in self.circuit.values():
            if pipe:
                pipe.draw(self.layer1)

        self.plop.draw(self.layer1)
        self.cursor.draw(self.layer1)
        self.liquid.draw(self.layer2)

        self.screen.blit(self.layer1, self.board_offset)
        self.screen.blit(self.layer2, self.board_offset)

        self.screen.blit(self.dashboard_left, (0, 0))
        self.screen.blit(
            self.dashboard_right,
            (self.screen.get_width() - self.dashboard_right.get_width(), 0)
        )

        self.score.draw(self.screen)
        self.countdown.draw(self.screen)

        self.arrow.draw(self.screen)

        for pipe in self.box:
            pipe.draw(self.screen)

        self.message_top.draw(self.screen)
        self.message_bottom.draw(self.screen)

        if self.state == 'WIN' or self.state == 'LOOSE':
            self.continue_btn.draw(self.screen)

        else:
            self.flood_btn.draw(self.screen)
            self.giveup_btn.draw(self.screen)

    def anim(self):
        """ Process some animations """

        self.plop.fly(-20)
        self.arrow.anim()

    # ## Buttons callbacks ## #

    def flood_now(self):
        """ Flood Button callback """

        self.sound.sub.play()
        pygame.time.set_timer(self.COUNTDOWN, 0)
        pygame.time.set_timer(self.FLOOD, 20)
        self.message_bottom.set_txt('HURRY !!!')

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
