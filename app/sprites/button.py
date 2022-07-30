from pygame import image as pgimage, mouse, mixer

from sprites.stamp import Stamp


class Button:
    """A menu button"""

    def __init__(self, labels, pos, onclick_function=None):
        self.labels = labels
        self.sound = mixer.Sound('./sounds/click.wav')
        self.images = []
        for i, label in enumerate(labels):
            image1 = pgimage.load('./images/button.png')
            image2 = pgimage.load('./images/button2.png')

            stamp = Stamp(label, 32, 'dark-grey',
                          (90, image1.get_height()/2), 'left')
            stamp.draw(image1)
            stamp.set_txt(label, 'red')
            stamp.draw(image2)

            self.images.append(image1)
            self.images.append(image2)

        self.pin = 0
        self.rect = self.images[0].get_rect()
        self.rect.midtop = pos
        self.glow = False
        self.onclick_function = onclick_function

    def process(self):
        """ Handle button behavior """

        if self.rect.collidepoint(mouse.get_pos()):
            if not self.glow:
                self.pin += 1
                self.glow = True

        else:
            if self.glow:
                self.pin -= 1
                self.glow = False

    def click(self):
        """ Execute button's callback if button is click """

        if self.glow:
            self.sound.play()
            if self.pin == len(self.images) - 1:
                self.pin = 1
            else:
                self.pin += 2
            return self.onclick_function()

    def draw(self, surface):
        """ Draw the button """

        surface.blit(self.images[self.pin], self.rect.topleft)
