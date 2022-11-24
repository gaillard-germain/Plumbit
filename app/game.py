import pygame
from random import choice

from factory import Factory
from box import Box
from circuit import Circuit
from config import (
    info, tile_size, board_tile_x, board_tile_y, max_time, min_time,
    flood_min_speed, flood_max_speed
)
from sprites.cursor import Cursor
from sprites.button import Button
from sprites.liquid import Liquid
from sprites.arrow import Arrow
from sprites.stamp import Stamp


class Game:
    def __init__(self, screen, function_quit):
        self.screen = screen
        self.quit = function_quit

        self.put = pygame.mixer.Sound('./sounds/put.ogg')
        self.switch = pygame.mixer.Sound('./sounds/switch.ogg')
        self.smash = pygame.mixer.Sound('./sounds/smash.ogg')
        self.match = pygame.mixer.Sound('./sounds/match.ogg')
        self.bip = pygame.mixer.Sound('./sounds/bip.ogg')
        self.tictac = pygame.mixer.Sound('./sounds/tictac.ogg')
        self.sub = pygame.mixer.Sound('./sounds/sub.ogg')
        self.loose = pygame.mixer.Sound('./sounds/loose.ogg')
        self.win = pygame.mixer.Sound('./sounds/win.ogg')

        self.music = True

        self.COUNTDOWN = pygame.USEREVENT + 1
        self.FLOOD = pygame.USEREVENT + 2
        self.ANIM = pygame.USEREVENT + 3

        self.lvl = 1
        self.time = max_time
        self.speed = flood_min_speed
        self.state = 'WAITING'

        self.dashboard_left = pygame.image.load('./images/dashboard_left.png')
        self.dashboard_right = pygame.image.load(
            './images/dashboard_right.png')

        self.layer1 = pygame.Surface(
            (tile_size*board_tile_x, tile_size*board_tile_y),
        )
        self.layer2 = pygame.Surface(
            (tile_size*board_tile_x, tile_size*board_tile_y),
            pygame.SRCALPHA,
            32
        )
        self.layer3 = pygame.Surface(
            (tile_size*board_tile_x, tile_size*board_tile_y),
            pygame.SRCALPHA,
            32
        )

        self.board = self.layer1.get_rect()

        self.board_offset = (
            (self.screen.get_width() - self.board.width)/2,
            (self.screen.get_height() - self.board.height)/2
        )

        self.factory = Factory(self.use_pipe, self.use_stopwatch,
                               self.use_wrench, self.use_bomb)
        self.box = Box(self.factory)
        self.circuit = Circuit(self.factory)
        self.cursor = Cursor(self.board_offset, self.circuit.is_locked)
        self.liquid = Liquid()
        self.arrow = Arrow()
        self.flood_btn = Button(['FLOOD'], (140, 50), 'light-blue',
                                self.flood_now)
        self.giveup_btn = Button(['GIVE-UP'], (140, 150), 'red', self.give_up)
        self.music_btn = Button(['MUSIC ON', 'MUSIC OFF'], (140, 250),
                                'light-blue', self.switch_music)
        self.continue_btn = Button(['CONTINUE'], (140, 50), 'green',
                                   self.next_step)
        self.score = Stamp(0, 40, 'green', (1673, 177))
        self.countdown = Stamp('', 40, 'light-blue', (1680, 900))
        self.message_top = Stamp('', 72, 'orange',
                                 (self.screen.get_width()/2, 100))
        self.message_bottom = Stamp('', 40, 'orange',
                                    (self.screen.get_width()/2,
                                     self.screen.get_height()-100))
        self.plop = Stamp('', 32)

        # ### dev tool ### #
        self.dev = Stamp('', 32, 'white',
                         (self.screen.get_width()/2,
                          self.screen.get_height()-50))
        # self.dev.set_txt('<text here>') # to display something...
        # ###### #

        self.valve = self.factory.get_valve()
        self.end = self.factory.get_end()

    def reset(self):
        """ Reset score, level and time """

        self.score.set_txt(0)
        self.lvl = 1
        self.time = max_time
        self.speed = flood_min_speed

        pygame.time.set_timer(self.ANIM, 15)
        self.set_up()

    def set_up(self):
        """ Set_up the game """

        self.state = 'WAITING'

        self.set_time()
        self.set_speed()

        self.layer2.fill((255, 255, 255, 0))

        self.box.fill()
        self.circuit.strew(self.valve, self.end, self.lvl)
        self.liquid.reset(self.valve)
        self.countdown.set_txt(self.time)
        self.message_top.set_txt('Level {}'.format(self.lvl))
        self.message_bottom.set_txt(
            'INFO: {}'.format(choice(info)))

        if self.music:
            pygame.mixer.music.play(loops=-1)

    def set_time(self):
        """ Decrease time """

        if self.time > min_time:
            self.time = max_time - (self.lvl - 1) * 2

    def set_speed(self):
        """ Increase flood speed """

        if self.speed > flood_max_speed:
            self.speed = flood_min_speed - (self.lvl - 1) * 2

    def on_mouse_click(self):
        """ Handle button click event """

        if self.state == 'LOOSE' or self.state == 'WIN':
            emit = self.continue_btn.click()

        else:
            self.music_btn.click()
            self.flood_btn.click()
            emit = self.giveup_btn.click()

            if (self.board.contains(self.cursor.rect)):
                self.box.get_current().use(self.cursor.rect.topleft)

        return emit

    def tic(self):
        """ Decrease countdown every second, and start flooding at 0 """

        self.tictac.play()
        self.valve.anim()
        self.countdown.set_txt(int(self.countdown.txt) - 1)
        if int(self.countdown.txt) <= 0:
            pygame.time.set_timer(self.COUNTDOWN, 0)
            pygame.time.set_timer(self.FLOOD, self.speed)
            self.sub.play()
            self.message_bottom.set_txt('HURRY !!!')

    def flood(self):
        """ Floods the circuit """

        pipe = self.liquid.flood(self.circuit.grid)

        if pipe == 'flooding':
            return

        elif pipe is None:
            self.lvl_failed()

        else:
            gain = pipe.gain

            if pipe == self.end:
                gain += int(self.countdown.txt) * 10
                self.lvl_complete()

            self.update_gain(pipe.rect.center, gain)

    def lvl_failed(self):
        """ When player loose """

        self.state = 'LOOSE'
        pygame.time.set_timer(self.COUNTDOWN, 0)
        pygame.time.set_timer(self.FLOOD, 0)
        pygame.mixer.music.stop()
        self.loose.play()
        self.message_top.set_txt('Level {} FAILED'.format(self.lvl))
        self.message_bottom.set_txt('Click CONTINUE button')
        pygame.event.clear()

    def lvl_complete(self):
        """ When player win """

        self.state = 'WIN'
        pygame.time.set_timer(self.FLOOD, 0)
        pygame.mixer.music.stop()
        self.win.play()
        self.message_top.set_txt('Level {} COMPLETE'.format(self.lvl))
        self.message_bottom.set_txt('Click CONTINUE button')
        self.lvl += 1
        pygame.event.clear()

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

    def draw(self):
        """ Draw every game things on screen """

        self.screen.fill((66, 63, 56))
        self.layer1.fill((96, 93, 86))
        self.layer3.fill((255, 255, 255, 0))

        self.circuit.draw(self.layer1)

        self.plop.draw(self.layer1)
        self.liquid.draw(self.layer2)
        self.cursor.draw(self.layer3)
        self.screen.blit(self.layer1, self.board_offset)
        self.screen.blit(self.layer2, self.board_offset)
        self.screen.blit(self.layer3, self.board_offset)
        self.screen.blit(self.dashboard_left, (0, 0))
        self.screen.blit(
            self.dashboard_right,
            (self.screen.get_width() - self.dashboard_right.get_width(), 0)
        )
        self.score.draw(self.screen)
        self.countdown.draw(self.screen)
        self.arrow.draw(self.screen)
        self.box.draw(self.screen)
        self.message_top.draw(self.screen)
        self.message_bottom.draw(self.screen)

        # ### dev tool ### #
        self.dev.draw(self.screen)
        # ###### #

        if self.state == 'WIN' or self.state == 'LOOSE':
            self.continue_btn.draw(self.screen)

        else:
            self.flood_btn.draw(self.screen)
            self.giveup_btn.draw(self.screen)
            self.music_btn.draw(self.screen)

    def anim(self):
        """ Process some animations """

        self.plop.fly(-20)
        self.arrow.anim()

    def process(self):
        """ Game's loop """

        pygame.mixer.music.load('./sounds/music.ogg')
        self.reset()

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.on_mouse_click() == 'BACK':
                        return

                if event.type == self.ANIM:
                    self.anim()

                if event.type == self.COUNTDOWN:
                    self.tic()

                if event.type == self.FLOOD:
                    self.flood()

            self.flood_btn.process()
            self.giveup_btn.process()
            self.music_btn.process()
            self.continue_btn.process()

            self.cursor.process(self.box.get_current())

            self.draw()

            pygame.display.update()
            clock.tick(30)

    # ## Callbacks ## #

    def switch_music(self):
        """ Music Button callback: Switch music ON or OFF """

        self.music = not self.music

        if self.music:
            pygame.mixer.music.play(loops=-1)
        else:
            pygame.mixer.music.stop()

    def flood_now(self):
        """ Flood Button callback: starts flooding the circuit """

        self.sub.play()
        pygame.time.set_timer(self.COUNTDOWN, 0)
        pygame.time.set_timer(self.FLOOD, flood_max_speed)
        self.message_bottom.set_txt('HURRY !!!')

    def give_up(self):
        """ Give-up Button callback: backs to menu """

        pygame.mixer.music.stop()
        pygame.time.set_timer(self.COUNTDOWN, 0)
        pygame.time.set_timer(self.FLOOD, 0)
        pygame.time.set_timer(self.ANIM, 0)

        return 'BACK'

    def next_step(self):
        """ Continue Button callback: Continue to next lvl or back to
            the menu """

        if self.state == 'WIN':
            self.set_up()

        elif self.state == 'LOOSE':
            return self.give_up()

    def use_pipe(self, pos):
        """ Pipe callback: place a pipe """

        if self.circuit.is_locked(pos):
            return

        if self.state == 'WAITING':
            self.state = 'RUNNING'
            pygame.time.set_timer(self.COUNTDOWN, 1000)
            self.message_bottom.set_txt('Incoming fluid...')

        pipe = self.box.pickup()

        self.put.play()
        pipe.rect.topleft = pos
        self.circuit.add(pipe)

        self.update_gain(pipe.rect.center, pipe.cost)

    def use_stopwatch(self, pos):
        """ Stopwatch callback: use a stopwatch """

        self.box.pickup()

        self.bip.play()
        pygame.time.set_timer(self.FLOOD, 0)
        self.countdown.set_txt(int(self.countdown.txt) + 5)

        if self.state != 'WAITING':
            pygame.time.set_timer(self.COUNTDOWN, 1000)

    def use_wrench(self, pos):
        """ Wrench callback: use a wrench """

        self.box.pickup()

        if self.circuit.is_mutable(pos):
            self.switch.play()
            self.circuit.rotate(pos, 1)
        else:
            self.match.play()

    def use_bomb(self, pos):
        """ Bomb callback: use a bomb """

        self.box.pickup()

        if self.circuit.is_mutable(pos):
            self.smash.play()
            self.circuit.delete(pos)
        else:
            self.match.play()
