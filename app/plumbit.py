import pygame
import sys

from game import Game
from menu import Menu
from record import Record


class Plumbit:
    """ Plumbit (the game loops) """

    def __init__(self):
        pygame.mixer.pre_init(buffer=2048)
        pygame.mixer.init()
        pygame.init()
        pygame.display.set_caption("Plumb'it")

        self.place = 'MENU'

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.game = Game(self.screen)
        self.record = Record(self.screen)
        self.menu = Menu(self.quit, self.screen, self.record.topten)

    def display_game(self):
        """ The game """

        self.game.reset()

        clock = pygame.time.Clock()

        while self.place == 'GAME':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.game.on_mouse_click() == 'LOOSE':
                        self.place = 'LOOSE'

                if event.type == self.game.ANIM:
                    self.game.anim()

                if event.type == self.game.COUNTDOWN:
                    self.game.tic()

                if event.type == self.game.FLOOD:
                    self.game.flood()

            self.game.process()

            pygame.display.update()
            clock.tick(60)

        next = self.record.check(int(self.game.score.txt), self.game.lvl)
        if next == 'MENU':
            self.place = 'MENU'
            return self.display_menu()
        elif next == 'RECORD':
            self.place = 'RECORD'
            return self.display_record()

    def display_menu(self):
        """ The menu with the TopTen """

        self.menu.display_topten()

        while self.place == 'MENU':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                elif (event.type == pygame.MOUSEBUTTONDOWN
                        and event.button == 1):
                    if self.menu.on_mouse_click() == 'GAME':
                        self.place = 'GAME'

            self.menu.process()

            pygame.display.update()

        return self.display_game()

    def display_record(self):
        """ Save the player's score in the TopTen """

        self.record.player_name = 'Enter your name'

        while self.place == 'RECORD':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.record.backspace()

                    elif event.key == pygame.K_RETURN:
                        self.record.save_score()
                        self.place = 'MENU'

                    else:
                        self.record.enter_name(event)

                elif (event.type == pygame.MOUSEBUTTONDOWN
                        and event.button == 1):
                    if self.record.on_mouse_click() == 'MENU':
                        self.place = 'MENU'

            self.record.process()

            pygame.display.update()

        return self.display_menu()

    def quit(self):
        """ Quit function """

        pygame.quit()
        sys.exit()


if __name__ == '__main__':
    Plumbit().display_menu()
