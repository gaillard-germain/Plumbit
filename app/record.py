import pygame
import os
import shutil
import json

from app.sprites.button import Button
from app.sprites.stamp import Stamp
from app.config import font_title


class Record:
    def __init__(self, screen, function_quit):
        self.applause = pygame.mixer.Sound('./sounds/applause.ogg')

        self.screen = screen
        self.quit = function_quit
        self.score = 0
        self.rank = None
        self.lvl = 1
        self.topten = None
        self.enter_btn = Button(
            ['ENTER'],
            (self.screen.get_width()/2, self.screen.get_height()/2 + 100),
            'green', self.save_score
        )
        self.title = Stamp('Well done!', 56, 'green',
                           (self.screen.get_width()/2,
                            self.screen.get_height()/2 - 300),
                           font_path=font_title)
        self.message = Stamp('', 48, 'light-blue',
                             (self.screen.get_width()/2,
                              self.screen.get_height()/2 - 100))
        self.name = Stamp('Enter your name', 40, 'red',
                          (self.screen.get_width()/2,
                           self.screen.get_height()/2))
        self.check_file()
        self.load_topten()

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

    @staticmethod
    def check_file():
        """ Check if topten.json exists, if not copy it from a clean file """

        if not os.path.exists('topten.json'):
            path = os.getcwd()
            src = '{}/topten_clean.json'.format(path)
            dst = '{}/topten.json'.format(path)

            shutil.copyfile(src, dst)

    def check(self, score, lvl):
        """ Checks if score may enter the TopTen """

        self.score = score
        self.lvl = lvl
        self.rank = None

        for index, player in enumerate(self.topten):
            if score > player["score"]:
                self.rank = index
                break

        if self.rank is not None:
            self.message.set_txt('{} is a new RECORD!'.format(self.score))
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

    def draw(self):
        """ Draw every record things on the screen """

        self.screen.fill((40, 42, 44))
        self.title.draw(self.screen)
        self.message.draw(self.screen)
        self.name.draw(self.screen)
        self.enter_btn.draw(self.screen)

    def process(self):
        """ Process Record """

        self.applause.play()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.backspace()

                    elif event.key == pygame.K_RETURN:
                        self.save_score()
                        return

                    else:
                        self.enter_name(event)

                elif (event.type == pygame.MOUSEBUTTONDOWN
                        and event.button == 1):
                    if self.on_mouse_click() == 'MENU':
                        return

            self.enter_btn.process()

            self.draw()

            pygame.display.update()

    # ## Buttons callbacks # ##

    def save_score(self):
        """ Enter Button callback """

        self.name.txt = self.name.txt.strip()

        if (self.name.txt == 'Enter your name'
                or not self.name.txt.replace(' ', '')):
            self.name.txt = 'Unknown'

        self.topten.insert(self.rank, dict(name=self.name.txt,
                           level=self.lvl,
                           score=self.score))
        if len(self.topten) > 10:
            del self.topten[-1]

        self.save_topten()

        return 'MENU'
