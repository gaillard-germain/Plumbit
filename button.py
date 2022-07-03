from pygame import image as pgimage, mouse
from tools import display_txt


class Button:
    """A menu button"""

    def __init__(self, label, pos, onclick_function=None):
        self.label = label
        self.image_1 = pgimage.load('images/button.png')
        display_txt(label, 40, (64, 68, 70), self.image_1, 100, 'center')
        self.image_2 = pgimage.load('images/button2.png')
        display_txt(label, 40, (194, 68, 25), self.image_2, 100, 'center')
        self.image = self.image_1
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.glow = False
        self.onclick_function = onclick_function
        self.clicked = False

    def process(self):
        if self.rect.collidepoint(mouse.get_pos()):
            if not self.glow:
                self.image = self.image_2
                self.glow = True

        else:
            if self.glow:
                self.image = self.image_1
                self.glow = False

    def click(self):
        if self.glow:
            self.onclick_function()
