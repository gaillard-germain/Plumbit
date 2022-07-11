import pygame
import sys

from sound import Sound
from tools import display_txt, new_record, load_json, update_json, check_topten
from button import Button
from game import Game


class Plumbit(object):
    """ Plumbit """

    def __init__(self):
        pygame.mixer.pre_init(buffer=2048)
        pygame.mixer.init()
        pygame.init()
        pygame.display.set_caption("Plumb'it")

        self.sound = Sound()

        self.player_name = 'Plumber'
        self.place = 'MENU'

        self.screen = None

        self.flood_btn = Button(
            'FLOOD', self.sound.click, (20, 50), self.flood_now)
        self.giveup_btn = Button(
            'GIVE-UP', self.sound.click, (20, 150), self.give_up)
        self.continue_btn = Button(
            'CONTINUE', self.sound.click, (20, 250), self.next_step)
        self.play_btn = Button('PLAY', self.sound.click, (180, 700), self.play)
        self.quit_btn = Button('QUIT', self.sound.click, (180, 800), self.quit)
        self.enter_btn = Button('ENTER', self.sound.click,
                                (195, 200), self.save_score)

        self.game = Game(self.flood_btn, self.giveup_btn, self.continue_btn)

        self.COUNTDOWN = pygame.USEREVENT + 1
        self.FLOOD = pygame.USEREVENT + 2
        self.ANIM = pygame.USEREVENT + 3

        check_topten()

    def main(self):
        """ main game """

        self.screen = pygame.display.set_mode((1440, 900))

        pygame.time.set_timer(self.ANIM, 15)

        clock = pygame.time.Clock()

        while self.place == 'GAME':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.game.state == 'LOOSE' or self.game.state == 'WIN':
                        self.continue_btn.click()

                    else:
                        self.flood_btn.click()
                        self.giveup_btn.click()

                        if self.game.state == 'WAITING':
                            self.game.state = 'RUNNING'
                            pygame.time.set_timer(self.COUNTDOWN, 1000)

                        if (self.game.board.collidepoint(
                            pygame.mouse.get_pos()
                        ) and self.game.drop_and_pickup()):
                            self.sound.put.play()

                if event.type == self.ANIM:
                    self.game.anim()

                if event.type == self.COUNTDOWN:
                    self.sound.tic.play()
                    self.game.countdown -= 1
                    self.game.valve.anim()
                    if self.game.countdown <= 0:
                        pygame.time.set_timer(self.COUNTDOWN, 0)
                        pygame.time.set_timer(self.FLOOD, 30)
                        self.sound.sub.play()

                if event.type == self.FLOOD:
                    self.game.flood()

                    if self.game.state == 'WIN':
                        pygame.time.set_timer(self.FLOOD, 0)
                        pygame.mixer.music.stop()
                        self.sound.win.play()

                    elif self.game.state == 'LOOSE':
                        pygame.time.set_timer(self.FLOOD, 0)
                        pygame.mixer.music.stop()
                        self.sound.loose.play()

            self.game.draw(self.screen)

            self.game.process()

            pygame.display.update()
            clock.tick(60)

        self.check_record()

    def menu(self):
        """ The menu with the TopTen """

        self.screen = pygame.display.set_mode((600, 900))
        self.screen.fill((40, 42, 44))

        display_txt("PLUMB'IT", 72, (170, 60, 60), self.screen, 'center', 50)

        for i, player in enumerate(load_json('topten.json')):
            display_txt(player["name"], 40, (50, 162, 162), self.screen, 140,
                        170 + i * 50)
            display_txt(player["score"], 40, (50, 162, 162), self.screen, 380,
                        170 + i * 50)
        while self.place == 'MENU':
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.play_btn.click()
                self.quit_btn.click()

            self.screen.blit(self.play_btn.image, self.play_btn.rect.topleft)
            self.screen.blit(self.quit_btn.image, self.quit_btn.rect.topleft)

            self.play_btn.process()
            self.quit_btn.process()

            pygame.display.update()

        return self.main()

    def entry(self):
        """ Save the player's score in the TopTen """

        self.screen = pygame.display.set_mode((600, 300))

        self.player_name = 'Enter your name'

        while self.place == 'ENTRY':
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.player_name) > 0:
                        self.player_name = self.player_name[:-1]

                elif event.key == pygame.K_RETURN:
                    self.save_score()

                else:
                    if self.player_name == 'Enter your name':
                        self.player_name = ''
                    if len(self.player_name) < 12:
                        self.player_name += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.enter_btn.click()

            self.screen.fill((40, 42, 44))
            txt = str(self.game.score) + ' is a new RECORD !'
            display_txt(txt, 48, (83, 162, 162), self.screen, 'center', 20)
            display_txt(self.player_name, 40, (170, 60, 60),
                        self.screen, 'center', 100)
            self.screen.blit(self.enter_btn.image, self.enter_btn.rect.topleft)

            self.enter_btn.process()

            pygame.display.update()

        return self.menu()

    def check_record(self):
        """ Checks if score may enter the TopTen """

        self.rank = new_record(self.game.score)
        if self.rank is not None:
            self.place = 'ENTRY'
            return self.entry()
        else:
            self.place = 'MENU'
            return self.menu()

# ## Buttons callbacks ## #

    def play(self):
        """ Play Button callback """

        self.game.reset()
        self.place = 'GAME'

    def quit(self):
        """ Quit Button callback """

        pygame.quit()
        sys.exit()

    def flood_now(self):
        """ Flood Button callback """

        self.sound.sub.play()
        pygame.time.set_timer(self.COUNTDOWN, 0)
        pygame.time.set_timer(self.FLOOD, 15)

    def give_up(self):
        """ Give-up Button callback """

        pygame.mixer.music.stop()
        pygame.time.set_timer(self.COUNTDOWN, 0)
        pygame.time.set_timer(self.FLOOD, 0)
        pygame.time.set_timer(self.ANIM, 0)
        self.place = 'ENTRY'

    def next_step(self):
        """ Continue Button callback """
        if self.game.state == 'WIN':
            self.game.set_up()

        elif self.game.state == 'LOOSE':
            self.give_up()

    def save_score(self):
        """ Enter Button callback """

        update_json(self.rank, self.player_name, self.game.score)
        self.place = 'MENU'


if __name__ == '__main__':
    Plumbit().menu()
