from pygame import image as pgimage, mouse, mixer

from tools import display_txt


class Button:
    """A menu button"""

    def __init__(self, label, pos, onclick_function=None):
        self.label = label
        self.sound = mixer.Sound('./sounds/click.wav')
        self.image_1 = pgimage.load('./images/button.png')
        self.image_2 = pgimage.load('./images/button2.png')
        display_txt(label, 32, (64, 68, 70), self.image_1, 100, None, 'left')
        display_txt(label, 32, (194, 68, 25), self.image_2, 100, None, 'left')
        self.image = self.image_1
        self.rect = self.image.get_rect()
        self.rect.midtop = pos
        self.glow = False
        self.onclick_function = onclick_function

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
            self.sound.play()
            return self.onclick_function()

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
