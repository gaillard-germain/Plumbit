from pygame import transform
from random import randint

from sprites.item import Item


class Pipe(Item):
    """ A Pipe """

    def __init__(self, data):
        super().__init__(data)
        self.apertures = data['apertures'].copy()
        self.cost = data['cost']
        self.gain = data['gain']
        self.modifier = data['modifier']
        self.locked = data['locked']
        self.immutable = data['immutable']

    def rotate(self, coef=0):
        """ Rotate the pipe (anti-clockwise)"""

        if not coef:
            coef = randint(0, 3)

        for i in range(coef):
            self.apertures.append(self.apertures.pop(0))
            for i, image in enumerate(self.images):
                self.images[i] = transform.rotate(image, 90)

    def align(self, pos):
        count = 0
        while pos not in self.open_to():
            count += 1
            self.rotate(1)
            if count == 3:
                break

    def open_to(self):
        """ Get the coordinates which where the pipe is open to """

        for index, aperture in enumerate(self.apertures):
            if aperture:
                if index == 0:
                    yield ((self.rect.left - self.rect.width), self.rect.top)
                if index == 1:
                    yield (self.rect.left, (self.rect.top - self.rect.height))
                if index == 2:
                    yield (self.rect.right, self.rect.top)
                if index == 3:
                    yield (self.rect.left, self.rect.bottom)

    def clog(self, path):
        """ Clogs the opening through which the liquid has passed """

        if path[0] < 0:
            self.apertures[2] = 0
        elif path[0] > 0:
            self.apertures[0] = 0
        if path[1] < 0:
            self.apertures[3] = 0
        elif path[1] > 0:
            self.apertures[1] = 0

        self.locked = True
