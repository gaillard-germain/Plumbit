import os
import shutil
import json
from tools import display_txt
from sprites.button import Button


class Record:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.rank = None
        self.player_name = 'Plumber'
        self.enter_btn = Button(
            'ENTER',
            (self.screen.get_width()/2, self.screen.get_height()/2 + 100),
            self.save_score
        )
        self.check_file()
        self.load_topten()

    def process(self):
        self.enter_btn.process()

        self.draw()

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

    def draw(self):
        self.screen.fill((40, 42, 44))
        txt = str(self.score) + ' is a new RECORD !'
        display_txt(txt, 48, (83, 162, 162), self.screen, None,
                    self.screen.get_height()/2 - 100)
        display_txt(self.player_name, 40, (170, 60, 60), self.screen)
        self.enter_btn.draw(self.screen)

    def check_file(self):
        """ Check if topten.json exists, if not copy it from a clean file """

        if not os.path.exists('topten.json'):
            path = os.getcwd()
            src = '{}/topten_clean.json'.format(path)
            dst = '{}/topten.json'.format(path)

            shutil.copyfile(src, dst)

    def check(self, score):
        """ Checks if score may enter the TopTen """

        self.score = score
        self.rank = None

        for index, player in enumerate(self.topten):
            if score > player["score"]:
                self.rank = index
                break

        if self.rank is not None:
            return 'RECORD'
        else:
            return 'MENU'

    def load_topten(self):
        """ Load the topten file """

        with open('./topten.json') as file:
            self.topten = json.load(file)

    def save_topten(self):
        """ Save the topten """

        with open('./topten.json', 'w') as file:
            json.dump(self.topten, file, indent=4)

    # ## Buttons callbacks # ##

    def save_score(self):
        """ Enter Button callback """

        self.topten.insert(self.rank, dict(name=self.player_name,
                           score=self.score))
        if len(self.topten) > 10:
            del self.topten[-1]

        self.save_topten()

        return 'MENU'
