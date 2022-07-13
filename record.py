from button import Button
from tools import display_txt, update_json, new_record


class Record:
    def __init__(self):
        self.score = 0
        self.rank = 0
        self.player_name = 'Plumber'
        self.enter_btn = Button('ENTER', (195, 200), self.save_score)

    def process(self):
        self.enter_btn.process()

    def on_mouse_click(self):
        emit = self.enter_btn.click()

        return emit

    def backspace(self):
        if len(self.player_name) > 0:
            self.player_name = self.player_name[:-1]

    def enter_name(self, event):
        if self.player_name == 'Enter your name':
            self.player_name = ''
        if len(self.player_name) < 12:
            self.player_name += event.unicode

    def draw(self, surface):
        surface.fill((40, 42, 44))
        txt = str(self.score) + ' is a new RECORD !'
        display_txt(txt, 48, (83, 162, 162), surface, 'center', 20)
        display_txt(self.player_name, 40, (170, 60, 60),
                    surface, 'center', 100)
        surface.blit(self.enter_btn.image, self.enter_btn.rect.topleft)

    def check(self, score):
        """ Checks if score may enter the TopTen """

        self.score = score
        self.rank = new_record(score)
        if self.rank is not None:
            return 'RECORD'
        else:
            return 'MENU'

    # ## Buttons callbacks # ##

    def save_score(self):
        """ Enter Button callback """

        update_json(self.rank, self.player_name, self.score)
        return 'MENU'
