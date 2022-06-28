from pygame import image as pgimage, transform
from random import randint, choices


class Pipe:
    """Un tuyau"""

    STOCK = {
        10: {
            'image': 'images/cross.png',
            'image2': None,
            'apertures': [1, 1, 1, 1],
            'name': 'cross'
        },
        40: {
            'image': 'images/regular_1.png',
            'image2': None,
            'apertures': [0, 1, 0, 1],
            'name': 'regular'
        },
        50: {
            'image': 'images/regular_2.png',
            'image2': None,
            'apertures': [0, 1, 1, 0],
            'name': 'regular'
            }
    }

    @classmethod
    def create(cls):
        ref = choices(list(cls.STOCK.values()), weights=cls.STOCK.keys(), k=1)
        return cls(ref[0])

    def __init__(self, ref):
        self.image = pgimage.load(ref['image'])
        if ref['image2']:
            self.image_2 = pgimage.load('images/valve_1a.png')
        else:
            self.image_2 = ref['image2']
        self.apertures = list(ref['apertures'])
        self.rect = self.image.get_rect()
        self.name = ref['name']
        self.locked = False

    def rotate(self):
        """Fait tourner le tuyau (anti-horaire)"""

        coef = randint(0, 3)
        for i in range(coef):
            self.apertures.append(self.apertures.pop(0))
            self.image = transform.rotate(self.image, 90)
            if self.image_2:
                self.image_2 = transform.rotate(self.image_2, 90)

        return self

    def open_to(self):
        """Pointe les coordonnees vers lesquels le tuyau est ouvert"""

        for index, aperture in enumerate(self.apertures):
            if aperture:
                if index == 0:
                    yield ((self.rect.left - 60), self.rect.top)
                if index == 1:
                    yield (self.rect.left, (self.rect.top - 60))
                if index == 2:
                    yield (self.rect.right, self.rect.top)
                if index == 3:
                    yield (self.rect.left, self.rect.bottom)

    def clog(self, path):
        """Bouche l'ouverture par laquelle le liquide est passé"""

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
        self.locked = True
