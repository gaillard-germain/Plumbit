from pygame import image as pgimage
from tools import display_txt


class Button:
    """A menu button"""

    def __init__(self, txt, pos):
        self.image_1 = pgimage.load('images/button.png')
        display_txt(txt, 40, (64, 68, 70), self.image_1, 100, 'center')
        self.image_2 = pgimage.load('images/button2.png')
        display_txt(txt, 40, (194, 68, 25), self.image_2, 100, 'center')
        self.image = self.image_1
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.glow = False

    def hover(self, mouse_pos):
        """ Change state if mouse is hover """
        x = False
        y = False
        if mouse_pos[0] > self.rect.left and mouse_pos[0] < self.rect.right:
            x = True
        if mouse_pos[1] > self.rect.top and mouse_pos[1] < self.rect.bottom:
            y = True
        if x and y:
            if not self.glow:
                self.image = self.image_2
                self.glow = True
        elif not x or not y:
            if self.glow:
                self.image = self.image_1
                self.glow = False
