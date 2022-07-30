from pygame import Surface, SRCALPHA

from sprites.button import Button
from sprites.stamp import Stamp


class Menu:
    def __init__(self, screen, topten, function_quit, function_music):
        self.screen = screen
        self.layer = Surface((self.screen.get_width()/3,
                             self.screen.get_height()/2), SRCALPHA, 32)
        self.music_btn = Button(
            ['MUSIC ON', 'MUSIC OFF'], (self.screen.get_width()/2, 800),
            function_music)
        self.play_btn = Button(
            ['PLAY'], (self.screen.get_width()/2, 880), self.play)
        self.quit_btn = Button(
            ['QUIT'], (self.screen.get_width()/2, 960), function_quit)
        self.topten = topten

        self.title = Stamp("PLUMB'IT", 72, 'red',
                           (self.screen.get_width()/2, 150))
        self.stamp = Stamp('', 40, 'light-blue')

    def process(self):
        """ Process buttons and drawing """

        self.music_btn.process()
        self.play_btn.process()
        self.quit_btn.process()

        self.draw()

    def on_mouse_click(self):
        """ Handle buttons click """

        self.music_btn.click()
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
            self.stamp.set_txt('lvl. {}'.format(player["level"]), pos=(
                self.layer.get_width()/2, i * 50 + 20))
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

        self.music_btn.draw(self.screen)
        self.play_btn.draw(self.screen)
        self.quit_btn.draw(self.screen)

    # ## Buttons callbacks # ##

    def play(self):
        """ Play Button callback """

        return 'GAME'

    def music(self):
        """ Music button callback """

        return 'MUSIC'
