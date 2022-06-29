#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Author: Germain GAILLARD <gaillard.germain@gmail.com>
# Version: 0.1
# License: MIT

"""Importation des modules"""
import sys
import pygame
from cursor import Cursor
from circuit import Circuit
from button import Button
from tools import display_txt, new_record, load_json, update_json
from sound import Sound


class Plumbit(object):
    """Plumbit"""

    def __init__(self):
        """initialise pygame et plumbit"""
        pygame.init()
        pygame.display.set_caption("Plumb'it")

        self.circuit = None
        self.sound = Sound()
        self.countdown = 60
        self.score = 0

        self.layer1 = pygame.Surface((900, 660), 32)
        self.layer2 = pygame.Surface((900, 660), pygame.SRCALPHA, 32)
        self.layer3 = pygame.Surface((134, 682), pygame.SRCALPHA, 32)

    def set_up(self):
        """Mise en place du plateau"""

        self.circuit = Circuit()
        self.layer2.fill((255, 255, 255, 0))
        self.sound.music.play()
        self.countdown = 60

    def main(self):
        """fonction principale, le jeu"""

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

        button = Button('FLOOD', (20, 50))
        button2 = Button('GIVE-UP', (20, 150))
        button3 = Button('CONTINUE', (20, 250))

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

                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    if not game_over:
                        button.hover(mouse_pos)
                        button2.hover(mouse_pos)
                        cursor.rect.topleft = cursor.confine(
                            board, mouse_pos)
                        cursor.hover_locked(self.circuit)
                    else:
                        button3.hover(mouse_pos)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and not game_over:
                        if self.countdown == 60:
                            pygame.time.set_timer(COUNTDOWN, 1000)
                        if button.glow:
                            self.sound.sub.play()
                            pygame.time.set_timer(COUNTDOWN, 0)
                            pygame.time.set_timer(FLOOD, 10)
                        elif button2.glow:
                            self.sound.music.stop()
                            pygame.time.set_timer(COUNTDOWN, 0)
                            pygame.time.set_timer(FLOOD, 0)
                            return self.menu()
                        elif not self.circuit.is_locked(cursor.rect.topleft):
                            self.sound.put.play()
                            self.circuit.drop_and_pickup(cursor.rect.topleft)
                            self.score -= 50

                    elif event.button == 1 and game_over:
                        if button3.glow:
                            if game_over == 'YOU WIN':
                                self.score += 500 + self.countdown * 10
                                self.set_up()
                                game_over = False

                            else:
                                rank = new_record(self.score)
                                if rank is not None:
                                    return self.entry(rank)
                                else:
                                    return self.menu()

                elif event.type == ANIM1:
                    self.circuit.anim_valve()

                elif event.type == ANIM2:
                    if arrow.left > 90:
                        arrow = arrow.move(-2, 0)
                    else:
                        arrow.left = 120

                elif event.type == COUNTDOWN:
                    self.sound.tic.play()
                    self.countdown -= 1
                    if self.countdown == 0:
                        pygame.time.set_timer(COUNTDOWN, 0)
                        pygame.time.set_timer(FLOOD, 30)
                        self.sound.sub.play()

                elif event.type == FLOOD:
                    game_over = self.circuit.flood()

                    if game_over == 'YOU WIN':
                        pygame.time.set_timer(FLOOD, 0)
                        self.sound.music.stop()
                        self.sound.win.play()

                    elif game_over == 'YOU LOOSE':
                        pygame.time.set_timer(FLOOD, 0)
                        self.sound.music.stop()
                        self.sound.loose.play()

                    elif game_over == 'PASS':
                        self.score += 100
                        game_over = False

            screen.fill((66, 63, 56))
            screen.blit(self.layer1, board.topleft)
            screen.blit(self.layer2, board.topleft)
            screen.blit(dashboard, (0, 0))
            screen.blit(self.layer3, (1167, 115))
            screen.blit(arrow_image, arrow.topleft)
            screen.blit(button.image, button.rect.topleft)
            screen.blit(button2.image, button2.rect.topleft)

            self.circuit.draw_box(screen)
            self.layer1.fill((96, 93, 86))
            self.circuit.draw_pipes(self.layer1)

            cursor.draw(self.layer1)
            self.circuit.draw_liquid(self.layer2)
            self.layer3.blit(back, (0, 0))

            display_txt(self.score, 40, (83, 162, 162), self.layer3,
                        'center', 5)
            display_txt(self.countdown, 40, (70, 170, 60), self.layer3,
                        'center', 625)
            if game_over:
                display_txt(game_over, 72, (194, 69, 26), screen,
                            'center', 20)
                txt = 'Click CONTINUE Button'
                display_txt(txt, 40, (194, 69, 26), screen,
                            'center', 800)
                screen.blit(button3.image, button3.rect.topleft)

            pygame.display.update()

    def menu(self):
        """Le menu, affiche le TopTen"""
        screen = pygame.display.set_mode((600, 900))
        screen.fill((40, 42, 44))
        topten = load_json('topten.json')
        button = Button('PLAY', (180, 700))
        button2 = Button('QUIT', (180, 800))
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
                button.hover(mouse_pos)
                button2.hover(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button.glow:
                        self.set_up()
                        break
                    elif button2.glow:
                        pygame.quit()
                        sys.exit()
            screen.blit(button.image, button.rect.topleft)
            screen.blit(button2.image, button2.rect.topleft)
            pygame.display.update()
        return self.main()

    def entry(self, rank):
        """Enregistre le nom du joueur dans le TopTen"""

        screen = pygame.display.set_mode((600, 300))
        button = Button('ENTER', (195, 200))
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
                    update_json(rank, name, self.score)
                    break
                else:
                    if name == 'Enter your name':
                        name = ''
                    if len(name) < 18:
                        name += event.unicode
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                button.hover(mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button.glow:
                        update_json(rank, name, self.score)
                        break

            screen.fill((40, 42, 44))
            txt = str(self.score) + ' is a new RECORD !'
            display_txt(txt, 48, (83, 162, 162), screen, 'center', 20)
            display_txt(name, 40, (170, 60, 60), screen, 'center', 100)
            screen.blit(button.image, button.rect.topleft)
            pygame.display.update()

        return self.menu()


if __name__ == '__main__':
    Plumbit().menu()
