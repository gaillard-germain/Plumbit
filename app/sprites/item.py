from pygame import Rect


class Item:
    """ An item """

    def __init__(self, data):
        self.name = data['name']
        self.size = 64
        self.images = data['images'].copy()
        self.pin = 0
        self.rect = Rect(0, 0, self.size, self.size)

    def draw(self, surface):
        """ Draw the item """

        surface.blit(self.images[self.pin], self.rect.topleft)

    def anim(self):
        """ Anim the item """

        length = len(self.images)
        if self.pin == length-1:
            self.pin = 0
        else:
            self.pin += 1
