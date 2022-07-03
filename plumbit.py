import pygame
import sys

from sound import Sound
from tools import display_txt, new_record, load_json, update_json
from button import Button
from game import Game


class Plumbit(object):
    """Plumbit"""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Plumb'it")

        self.screen = None

        self.game = Game()
        self.sound = Sound()

        self.COUNTDOWN = pygame.USEREVENT + 1
        self.FLOOD = pygame.USEREVENT + 2

    def set_up(self):
        """ Set_up the game """

        self.game.set_up()
        self.sound.music.play(loops=-1)

    def main(self):
        """ main game """

        self.screen = pygame.display.set_mode((1440, 900))

        ANIM = pygame.USEREVENT + 3

        flood_btn = Button('FLOOD', (20, 50), self.flood_now)
        giveup_btn = Button('GIVE-UP', (20, 150), self.give_up)
        continue_btn = Button('CONTINUE', (20, 250), self.next_step)

        pygame.time.set_timer(ANIM, 15)

        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    if self.game.state == 'LOOSE' or self.game.state == 'WIN':
                        continue_btn.click()

                    else:
                        flood_btn.click()
                        giveup_btn.click()

                        if self.game.state == 'WAITING':
                            self.game.state = 'RUNNING'
                            pygame.time.set_timer(self.COUNTDOWN, 1000)

                        if (self.game.board.collidepoint(
                            pygame.mouse.get_pos()
                        ) and self.game.drop_and_pickup()):
                            self.sound.put.play()

                if event.type == ANIM:
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
                        self.sound.music.stop()
                        self.sound.win.play()

                    elif self.game.state == 'LOOSE':
                        pygame.time.set_timer(self.FLOOD, 0)
                        self.sound.music.stop()
                        self.sound.loose.play()

            self.screen.fill((66, 63, 56))

            self.game.draw(self.screen, continue_btn)

            self.screen.blit(flood_btn.image, flood_btn.rect.topleft)
            self.screen.blit(giveup_btn.image, giveup_btn.rect.topleft)

            flood_btn.process()
            giveup_btn.process()
            continue_btn.process()

            self.game.process()

            pygame.display.update()
            clock.tick(60)

    def menu(self):
        """ The menu with the TopTen """

        self.screen = pygame.display.set_mode((600, 900))
        self.screen.fill((40, 42, 44))
        topten = load_json('topten.json')
        play_btn = Button('PLAY', (180, 700), self.play)
        quit_btn = Button('QUIT', (180, 800), self.quit)
        txt = "PLUMB'IT"

        display_txt(txt, 72, (170, 60, 60), self.screen, 'center', 50)
        for i, player in enumerate(topten):
            display_txt(player["name"], 40, (50, 162, 162), self.screen, 140,
                        170 + i * 50)
            display_txt(player["score"], 40, (50, 162, 162), self.screen, 380,
                        170 + i * 50)
        while True:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                self.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                play_btn.click()
                quit_btn.click()

            self.screen.blit(play_btn.image, play_btn.rect.topleft)
            self.screen.blit(quit_btn.image, quit_btn.rect.topleft)

            play_btn.process()
            quit_btn.process()

            pygame.display.update()

    def entry(self):
        """ Save the player's score in the TopTen """

        self.screen = pygame.display.set_mode((600, 300))
        enter_btn = Button('ENTER', (195, 200), self.save_score)
        self.player_name = 'Enter your name'

        while True:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.player_name) > 0:
                        self.player_name = self.player_name[:-1]

                elif event.key == pygame.K_RETURN:
                    update_json(self.rank, self.player_name,
                                self.game.score)
                    return self.menu()
                else:
                    if self.player_name == 'Enter your name':
                        self.player_name = ''
                    if len(self.player_name) < 18:
                        self.player_name += event.unicode

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                enter_btn.click()

            self.screen.fill((40, 42, 44))
            txt = str(self.game.score) + ' is a new RECORD !'
            display_txt(txt, 48, (83, 162, 162), self.screen, 'center', 20)
            display_txt(self.player_name, 40, (170, 60, 60),
                        self.screen, 'center', 100)
            self.screen.blit(enter_btn.image, enter_btn.rect.topleft)

            enter_btn.process()

            pygame.display.update()

# ## Buttons callbacks ## #

    def play(self):
        self.game.reset()
        self.set_up()
        return self.main()

    def quit(self):
        pygame.quit()
        sys.exit()

    def flood_now(self):
        self.sound.sub.play()
        pygame.time.set_timer(self.COUNTDOWN, 0)
        pygame.time.set_timer(self.FLOOD, 15)

    def give_up(self):
        self.sound.music.stop()
        pygame.time.set_timer(self.COUNTDOWN, 0)
        pygame.time.set_timer(self.FLOOD, 0)
        self.check_record()

    def next_step(self):
        if self.game.state == 'WIN':
            self.set_up()

        elif self.game.state == 'LOOSE':
            self.check_record()

    def check_record(self):
        self.rank = new_record(self.game.score)
        if self.rank is not None:
            return self.entry(self.rank)
        else:
            return self.menu()

    def save_score(self):
        update_json(self.rank, self.player_name, self.game.score)
        return self.menu()


if __name__ == '__main__':
    Plumbit().menu()
