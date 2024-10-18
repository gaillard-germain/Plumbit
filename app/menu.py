import pygame

from app.sprites.button import Button
from app.sprites.stamp import Stamp
from app.config import font_title


class Menu:
    def __init__(self, screen, topten, function_quit):
        self.screen = screen
        self.topten = topten
        self.quit = function_quit
        self.layer = pygame.Surface((self.screen.get_width()/3,
                                    self.screen.get_height()/2),
                                    pygame.SRCALPHA, 32)
        self.play_btn = Button(
            ['PLAY'], (self.screen.get_width()/2, 800), 'green', self.play)
        self.quit_btn = Button(
            ['QUIT'], (self.screen.get_width()/2, 900), 'red', function_quit)

        self.title = Stamp("PLUMB'IT", 72, 'red',
                           (self.screen.get_width()/2, 150),
                           font_path=font_title)
        self.stamp = Stamp('', 40, 'light-blue')

    def on_mouse_click(self):
        """ Handle buttons click """

        emit = self.play_btn.click()
        self.quit_btn.click()

        return emit

    def display_topten(self):
        """ display the topten """

        self.layer.fill((255, 255, 255, 0))
        for i, player in enumerate(self.topten):
            self.stamp.set_txt(player["name"], pos=(
                0, i * 50 + 20), alignement='left')
            self.stamp.draw(self.layer)
            self.stamp.set_txt('lvl. {}'.format(player["level"]), pos=(
                self.layer.get_width()/2, i * 50 + 20))
            self.stamp.draw(self.layer)
            self.stamp.set_txt(player["score"], pos=(
                self.layer.get_width(), i * 50 + 20), alignement='right')
            self.stamp.draw(self.layer)

    def draw(self):
        """ Draw every menu things on the screen """

        self.screen.fill((40, 42, 44))

        self.title.draw(self.screen)

        self.screen.blit(
            self.layer,
            ((self.screen.get_width() - self.layer.get_width())/2,
             (self.screen.get_height() - self.layer.get_height())/2)
        )
        self.play_btn.draw(self.screen)
        self.quit_btn.draw(self.screen)

    def process(self):
        """ Process Menu """

        self.display_topten()

        pygame.mixer.music.load('./sounds/water-drops.ogg')
        pygame.mixer.music.play(loops=-1)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                elif (event.type == pygame.MOUSEBUTTONDOWN
                        and event.button == 1):
                    if self.on_mouse_click() == 'GAME':
                        pygame.mixer.music.stop()
                        return

            self.play_btn.process()
            self.quit_btn.process()

            self.draw()

            pygame.display.update()

    # ## Buttons callbacks # ##

    def play(self):
        """ Play Button callback """

        return 'GAME'
