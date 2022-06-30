import pygame
import sys

from sound import Sound
from tools import display_txt, new_record, load_json, update_json
from button import Button
from circuit import Circuit
from cursor import Cursor


class Plumbit(object):
    """Plumbit"""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Plumb'it")

        self.circuit = Circuit()
        self.sound = Sound()
        self.countdown = 60

        self.layer1 = pygame.Surface((900, 660), 32)
        self.layer2 = pygame.Surface((900, 660), pygame.SRCALPHA, 32)
        self.layer3 = pygame.Surface((134, 682), pygame.SRCALPHA, 32)

    def set_up(self):
        """ Set_up the game """

        self.circuit.set_up()
        self.layer2.fill((255, 255, 255, 0))
        self.sound.music.play()
        self.countdown = 60 - self.circuit.lvl

    def main(self):
        """ main game """

        screen = pygame.display.set_mode((1440, 900))

        COUNTDOWN = pygame.USEREVENT + 1
        FLOOD = pygame.USEREVENT + 2
        ANIM1 = pygame.USEREVENT + 3
        ANIM2 = pygame.USEREVENT + 4

        dashboard = pygame.image.load('images/dashboard.png')
        back = pygame.image.load('images/dashboard_back.png')
        arrow_image = pygame.image.load('images/arrow.png')

        cursor = Cursor()
        board = self.layer1.get_rect()
        arrow = arrow_image.get_rect()

        flood_btn = Button('FLOOD', (20, 50))
        giveup_btn = Button('GIVE-UP', (20, 150))
        continue_btn = Button('CONTINUE', (20, 250))

        board.topleft = (250, 120)
        arrow.topleft = (120, 485)

        game_over = False

        pygame.time.set_timer(ANIM1, 500)
        pygame.time.set_timer(ANIM2, 30)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if not game_over:
                        flood_btn.hover(mouse_pos)
                        giveup_btn.hover(mouse_pos)
                        cursor.rect.topleft = cursor.confine(
                            board, mouse_pos)
                        cursor.hover_locked(self.circuit)
                    else:
                        continue_btn.hover(mouse_pos)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not game_over:
                        if self.countdown == 60 - self.circuit.lvl:
                            pygame.time.set_timer(COUNTDOWN, 1000)
                        if flood_btn.glow:
                            self.sound.sub.play()
                            pygame.time.set_timer(COUNTDOWN, 0)
                            pygame.time.set_timer(FLOOD, 10)
                        elif giveup_btn.glow:
                            self.sound.music.stop()
                            pygame.time.set_timer(COUNTDOWN, 0)
                            pygame.time.set_timer(FLOOD, 0)
                            return self.menu()
                        elif not self.circuit.is_locked(cursor.rect.topleft):
                            self.sound.put.play()
                            self.circuit.drop_and_pickup(cursor.rect.topleft)

                    elif event.button == 1 and game_over:
                        if continue_btn.glow:
                            if game_over == 'YOU WIN':
                                self.set_up()
                                game_over = False

                            else:
                                rank = new_record(self.circuit.score)
                                if rank is not None:
                                    return self.entry(rank)
                                else:
                                    return self.menu()

                if event.type == ANIM1:
                    self.circuit.valve.anim()

                if event.type == ANIM2:
                    if arrow.left > 90:
                        arrow = arrow.move(-2, 0)
                    else:
                        arrow.left = 120

                if event.type == COUNTDOWN:
                    self.sound.tic.play()
                    self.countdown -= 1
                    if self.countdown == 0:
                        pygame.time.set_timer(COUNTDOWN, 0)
                        pygame.time.set_timer(FLOOD, 30)
                        self.sound.sub.play()

                if event.type == FLOOD:
                    state = self.circuit.flood()

                    if state == 'YOU WIN':
                        pygame.time.set_timer(FLOOD, 0)
                        self.sound.music.stop()
                        self.sound.win.play()
                        game_over = 'YOU WIN'

                    elif state == 'YOU LOOSE':
                        pygame.time.set_timer(FLOOD, 0)
                        self.sound.music.stop()
                        self.sound.loose.play()
                        game_over = 'YOU LOOSE'

            screen.fill((66, 63, 56))
            screen.blit(self.layer1, board.topleft)
            screen.blit(self.layer2, board.topleft)
            screen.blit(dashboard, (0, 0))
            screen.blit(self.layer3, (1167, 115))
            screen.blit(arrow_image, arrow.topleft)
            screen.blit(flood_btn.image, flood_btn.rect.topleft)
            screen.blit(giveup_btn.image, giveup_btn.rect.topleft)

            self.circuit.draw_box(screen)
            self.layer1.fill((96, 93, 86))
            self.circuit.draw_pipes(self.layer1)

            cursor.draw(self.layer1)
            self.circuit.draw_liquid(self.layer2)
            self.layer3.blit(back, (0, 0))

            display_txt(self.circuit.score, 40, (83, 162, 162), self.layer3,
                        'center', 5)
            display_txt(self.countdown, 40, (70, 170, 60), self.layer3,
                        'center', 625)

            if game_over:
                display_txt(game_over, 72, (194, 69, 26), screen,
                            'center', 20)
                txt = 'Click CONTINUE Button'
                display_txt(txt, 40, (194, 69, 26), screen,
                            'center', 800)
                screen.blit(continue_btn.image, continue_btn.rect.topleft)

            pygame.display.update()

    def menu(self):
        """ The menu with the TopTen """
        screen = pygame.display.set_mode((600, 900))
        screen.fill((40, 42, 44))
        topten = load_json('topten.json')
        play_btn = Button('PLAY', (180, 700))
        quit_btn = Button('QUIT', (180, 800))
        txt = "PLUMB'IT"
        display_txt(txt, 72, (170, 60, 60), screen, 'center', 50)
        for i, player in enumerate(topten):
            display_txt(player["name"], 40, (50, 162, 162), screen, 140,
                        170 + i * 50)
            display_txt(player["score"], 40, (50, 162, 162), screen, 380,
                        170 + i * 50)
        while True:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                play_btn.hover(mouse_pos)
                quit_btn.hover(mouse_pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if play_btn.glow:
                        self.circuit.reset()
                        self.set_up()
                        break

                    elif quit_btn.glow:
                        pygame.quit()
                        sys.exit()

            screen.blit(play_btn.image, play_btn.rect.topleft)
            screen.blit(quit_btn.image, quit_btn.rect.topleft)
            pygame.display.update()

        return self.main()

    def entry(self, rank):
        """ Save the player's score in the TopTen """

        screen = pygame.display.set_mode((600, 300))
        enter_btn = Button('ENTER', (195, 200))
        name = 'Enter your name'
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(name) > 0:
                        name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    update_json(rank, name, self.circuit.score)
                    break
                else:
                    if name == 'Enter your name':
                        name = ''
                    if len(name) < 18:
                        name += event.unicode
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                enter_btn.hover(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if enter_btn.glow:
                        update_json(rank, name, self.circuit.score)
                        break

            screen.fill((40, 42, 44))
            txt = str(self.circuit.score) + ' is a new RECORD !'
            display_txt(txt, 48, (83, 162, 162), screen, 'center', 20)
            display_txt(name, 40, (170, 60, 60), screen, 'center', 100)
            screen.blit(enter_btn.image, enter_btn.rect.topleft)
            pygame.display.update()

        return self.menu()


if __name__ == '__main__':
    Plumbit().menu()
