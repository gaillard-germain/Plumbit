from tools import display_txt, load_topten
from sprites.button import Button


class Menu:
    def __init__(self, function_quit, screen):
        self.screen = screen
        self.quit = function_quit
        self.play_btn = Button(
            'PLAY', (self.screen.get_width()/2, 700), self.play)
        self.quit_btn = Button(
            'QUIT', (self.screen.get_width()/2, 800), self.quit)

    def process(self):
        self.play_btn.process()
        self.quit_btn.process()

        self.draw()

    def on_mouse_click(self):
        emit = self.play_btn.click()
        self.quit_btn.click()

        return emit

    def draw(self):
        self.screen.fill((40, 42, 44))

        display_txt("PLUMB'IT", 72, (170, 60, 60), self.screen, None, 50)

        for i, player in enumerate(load_topten()):
            display_txt(player["name"], 40, (50, 162, 162), self.screen,
                        self.screen.get_width()/2 - 200, 170 + i * 50, 'left')
            display_txt(player["score"], 40, (50, 162, 162), self.screen,
                        self.screen.get_width()/2 + 200,
                        170 + i * 50, 'right')

        self.play_btn.draw(self.screen)
        self.quit_btn.draw(self.screen)

    # ## Buttons callbacks # ##

    def play(self):
        """ Play Button callback """

        return 'GAME'
