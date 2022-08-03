from pygame import transform
from random import randint

from sprites.item import Item


class Block(Item):
    """ A Block """

    def __init__(self, data):
        super().__init__(data)
        self.locked = data['locked']
        self.immutable = data['immutable']

    def rotate(self, coef):
        for i in range(coef):
            for i, image in enumerate(self.images):
                self.images[i] = transform.rotate(image, 90)

    def randomize_image(self):
        """ Select a random image for a pipe """

        self.pin = randint(0, len(self.images)-1)
