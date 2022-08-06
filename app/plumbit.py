import pygame
import sys

from game import Game
from menu import Menu
from record import Record


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
        self.menu = Menu(self.screen, self.record.topten, self.quit,
                         self.game.switch_music)

    def display_game(self):
        """ The game """

        self.game.process()

        next = self.record.check(int(self.game.score.txt), self.game.lvl)
        if next == 'MENU':
            return self.display_menu()
        elif next == 'RECORD':
            return self.display_record()

    def display_menu(self):
        """ The menu with the TopTen """

        self.menu.process()

        return self.display_game()

    def display_record(self):
        """ Save the player's score in the TopTen """

        self.record.process()

        return self.display_menu()

    def quit(self):
        """ Quit function """

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    Plumbit().display_menu()
