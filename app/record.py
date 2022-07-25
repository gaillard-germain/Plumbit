import os
import shutil
import json

from sprites.button import Button
from sprites.stamp import Stamp


class Record:
    def __init__(self, screen):
        self.screen = screen
        self.score = 0
        self.rank = None
        self.enter_btn = Button(
            'ENTER',
            (self.screen.get_width()/2, self.screen.get_height()/2 + 100),
            self.save_score
        )
        self.title = Stamp('', 48, 'light-blue',
                           (self.screen.get_width()/2,
                            self.screen.get_height()/2 - 100))
        self.name = Stamp('Enter your name', 40, 'red',
                          (self.screen.get_width()/2,
                           self.screen.get_height()/2))
        self.check_file()
        self.load_topten()

    def process(self):
        """ Process buttons and drawing """

        self.enter_btn.process()

        self.draw()

    def on_mouse_click(self):
        """ Handle buttons click """

        emit = self.enter_btn.click()

        return emit

    def backspace(self):
        """ User entry correction """

        if len(self.name.txt) > 0:
            self.name.set_txt(self.name.txt[:-1])

    def enter_name(self, event):
        """ User entry """

        if self.name.txt == 'Enter your name':
            self.name.set_txt('')
        if len(self.name.txt) < 12:
            self.name.set_txt(self.name.txt + event.unicode)

    def draw(self):
        """ Draw every record things on the screen """

        self.screen.fill((40, 42, 44))
        self.title.draw(self.screen)
        self.name.draw(self.screen)
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
            self.title.set_txt('{} is a new RECORD!'.format(self.score))
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

        self.topten.insert(self.rank, dict(name=self.name.txt,
                           score=self.score))
        if len(self.topten) > 10:
            del self.topten[-1]

        self.save_topten()

        return 'MENU'
