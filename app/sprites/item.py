from pygame import Rect

from config import tile_size


class Item:
    """ An item """

    def __init__(self, data):
        self.name = data['name']
        self.images = data['images'].copy()
        self.pin = 0
        self.rect = Rect(0, 0, tile_size, tile_size)
        self.use = data['callback']

    def draw(self, surface):
        """ Blit the item on the surface """

        surface.blit(self.images[self.pin], self.rect.topleft)

    def anim(self):
        """ Anim the item """

        if self.pin == len(self.images)-1:
            self.pin = 0
        else:
            self.pin += 1
