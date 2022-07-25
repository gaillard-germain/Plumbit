from pygame import Surface, SRCALPHA

from sprites.button import Button
from sprites.stamp import Stamp


class Menu:
    def __init__(self, function_quit, screen, topten):
        self.screen = screen
        self.layer = Surface((self.screen.get_width()/3,
                             self.screen.get_height()/2), SRCALPHA, 32)
        self.quit = function_quit
        self.play_btn = Button(
            'PLAY', (self.screen.get_width()/2, 800), self.play)
        self.quit_btn = Button(
            'QUIT', (self.screen.get_width()/2, 900), self.quit)
        self.topten = topten

        self.title = Stamp("PLUMB'IT", 72, 'red',
                           (self.screen.get_width()/2, 150))
        self.stamp = Stamp('', 40, 'light-blue')

    def process(self):
        """ Process buttons and drawing """

        self.play_btn.process()
        self.quit_btn.process()

        self.draw()

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
                0, i * 50 + 20), align='left')
            self.stamp.draw(self.layer)
            self.stamp.set_txt(player["score"], pos=(
                self.layer.get_width(), i * 50 + 20), align='right')
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

    # ## Buttons callbacks # ##

    def play(self):
        """ Play Button callback """

        return 'GAME'
