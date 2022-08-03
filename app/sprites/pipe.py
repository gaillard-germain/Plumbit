from pygame import transform, Rect
from random import randint


class Pipe:
    """ A Pipe """

    def __init__(self, data):
        self.size = 64
        self.images = data['images'].copy()
        self.pin = 0
        self.apertures = data['apertures'].copy()
        self.name = data['name']
        self.cost = data['cost']
        self.gain = data['gain']
        self.modifier = data['modifier']
        self.locked = data['locked']
        self.immutable = data['immutable']
        self.rect = Rect(0, 0, self.size, self.size)

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

    def draw(self, surface):
        """ Draw the pipe """

        surface.blit(self.images[self.pin], self.rect.topleft)

    def anim(self):
        """ Anim the pipe """

        length = len(self.images)
        if self.pin == length-1:
            self.pin = 0
        else:
            self.pin += 1

    def randomize_image(self):
        """ Select a random image for a pipe """

        self.pin = randint(0, len(self.images)-1)
