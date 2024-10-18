import pygame
import sys

from app.game import Game
from app.menu import Menu
from app.record import Record


class Plumbit:
    """ Plumbit """

    def __init__(self):
        pygame.mixer.pre_init()
        pygame.mixer.init()
        pygame.init()
        pygame.mixer.music.set_volume(0.5)
        pygame.display.set_caption("Plumb'it")

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.game = Game(self.screen, self.quit)
        self.record = Record(self.screen, self.quit)
        self.menu = Menu(self.screen, self.record.topten, self.quit)

    def display_game(self):
        """ The game """

        self.game.process()

        next_step = self.record.check(int(self.game.score.txt), self.game.lvl)

        if next_step == 'MENU':
            return self.display_menu()

        elif next_step == 'RECORD':
            return self.display_record()

    def display_menu(self):
        """ The menu with the TopTen """

        self.menu.process()

        return self.display_game()

    def display_record(self):
        """ Save the player's score in the TopTen """

        self.record.process()

        return self.display_menu()

    @staticmethod
    def quit():
        """ Quit function """

        pygame.quit()
        sys.exit()
