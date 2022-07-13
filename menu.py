from button import Button
from tools import display_txt, load_json


class Menu:
    def __init__(self, function_quit):
        self.quit = function_quit
        self.play_btn = Button('PLAY', (180, 700), self.play)
        self.quit_btn = Button('QUIT', (180, 800), self.quit)

    def process(self):
        self.play_btn.process()
        self.quit_btn.process()

    def on_mouse_click(self):
        emit = self.play_btn.click()
        self.quit_btn.click()

        return emit

    def draw(self, surface):
        surface.fill((40, 42, 44))

        display_txt("PLUMB'IT", 72, (170, 60, 60), surface, 'center', 50)

        for i, player in enumerate(load_json('topten.json')):
            display_txt(player["name"], 40, (50, 162, 162), surface, 140,
                        170 + i * 50)
            display_txt(player["score"], 40, (50, 162, 162), surface, 380,
                        170 + i * 50)

        surface.blit(self.play_btn.image, self.play_btn.rect.topleft)
        surface.blit(self.quit_btn.image, self.quit_btn.rect.topleft)

    # ## Buttons callbacks # ##

    def play(self):
        """ Play Button callback """

        return 'GAME'
