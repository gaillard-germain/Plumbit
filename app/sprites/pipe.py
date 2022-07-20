from pygame import transform
from random import randint


class Pipe:
    """ A Pipe """

    def __init__(self, data):
        self.image = data['image']
        self.image_2 = data['image2']
        self.apertures = data['apertures'].copy()
        self.name = data['name']
        self.cost = data['cost']
        self.gain = data['gain']
        self.locked = data['locked']
        self.rect = self.image.get_rect()
        self.flooded = False

    def rotate(self, coef=0):
        """ Rotate the pipe (anti-clockwise)"""

        if not coef:
            coef = randint(0, 3)
        for i in range(coef):
            self.apertures.append(self.apertures.pop(0))
            self.image = transform.rotate(self.image, 90)
            if self.image_2:
                self.image_2 = transform.rotate(self.image_2, 90)

        return self

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

        self.lock()

    def lock(self):
        """ Locks the pipe """

        self.locked = True

    def anim(self):
        """ Animates the starting valve """

        if self.image_2:
            self.image, self.image_2 = (self.image_2, self.image)