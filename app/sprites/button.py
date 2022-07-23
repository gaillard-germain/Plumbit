from pygame import image as pgimage, mouse, mixer

from sprites.stamp import Stamp


class Button:
    """A menu button"""

    def __init__(self, label, pos, onclick_function=None):
        self.label = label
        self.sound = mixer.Sound('./sounds/click.wav')
        self.images = [
            pgimage.load('./images/button.png'),
            pgimage.load('./images/button2.png')
        ]
        self.pin = 0
        self.rect = self.images[0].get_rect()
        self.rect.midtop = pos
        self.glow = False
        self.onclick_function = onclick_function

        stamp = Stamp(label, 32, 'dark-grey',
                      (90, self.rect.height/2), 'left')
        stamp.draw(self.images[0])
        stamp.set_txt(label, 'red')
        stamp.draw(self.images[1])

    def process(self):
        if self.rect.collidepoint(mouse.get_pos()):
            if not self.glow:
                self.pin = 1
                self.glow = True

        else:
            if self.glow:
                self.pin = 0
                self.glow = False

    def click(self):
        if self.glow:
            self.sound.play()
            return self.onclick_function()

    def draw(self, surface):
        surface.blit(self.images[self.pin], self.rect.topleft)
