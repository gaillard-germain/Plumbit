from pygame import image as pgimage
from random import choices
from pipe import Pipe


class Factory:
    def __init__(self):
        self.stock = [
            {
                'image': pgimage.load('images/cross.png'),
                'image2': None,
                'apertures': [1, 1, 1, 1],
                'name': 'cross',
                'cost': -75,
                'gain': 100,
                'locked': False,
                'weight': 30
            },
            {
                'image': pgimage.load('images/regular_tb.png'),
                'image2': None,
                'apertures': [0, 1, 0, 1],
                'name': 'straight',
                'cost': -50,
                'gain': 100,
                'locked': False,
                'weight': 50
            },
            {
                'image': pgimage.load('images/regular_lr.png'),
                'image2': None,
                'apertures': [1, 0, 1, 0],
                'name': 'straight',
                'cost': -50,
                'gain': 100,
                'locked': False,
                'weight': 50
            },
            {
                'image': pgimage.load('images/regular_tr.png'),
                'image2': None,
                'apertures': [0, 1, 1, 0],
                'name': 'elbow',
                'cost': -50,
                'gain': 100,
                'locked': False,
                'weight': 40
            },
            {
                'image': pgimage.load('images/regular_tl.png'),
                'image2': None,
                'apertures': [1, 1, 0, 0],
                'name': 'elbow',
                'cost': -50,
                'gain': 100,
                'locked': False,
                'weight': 40
            },
            {
                'image': pgimage.load('images/regular_br.png'),
                'image2': None,
                'apertures': [0, 0, 1, 1],
                'name': 'elbow',
                'cost': -50,
                'gain': 100,
                'locked': False,
                'weight': 40
            },
            {
                'image': pgimage.load('images/regular_bl.png'),
                'image2': None,
                'apertures': [1, 0, 0, 1],
                'name': 'elbow',
                'cost': -50,
                'gain': 100,
                'locked': False,
                'weight': 40
            }
        ]
        self.extra = {
            'valve': {
                'image': pgimage.load('images/valve_1a.png'),
                'image2': pgimage.load('images/valve_1.png'),
                'apertures': [0, 0, 1, 0],
                'name': 'valve',
                'cost': 0,
                'gain': 0,
                'locked': True,
            },
            'end': {
                'image': pgimage.load('images/valve_2.png'),
                'image2': None,
                'apertures': [0, 0, 1, 0],
                'name': 'end',
                'cost': 0,
                'gain': 300,
                'locked': True,
            },
            'block': {
                'image': pgimage.load('images/block.png'),
                'image2': None,
                'apertures': [],
                'name': 'block',
                'cost': 0,
                'gain': 0,
                'locked': True,
            }
        }

    def get_extra(self, name):
        """ Return a special pipe """

        return Pipe(self.extra[name])

    def get_pipe(self):
        """ Return a random pipe """

        data = choices(self.stock,
                       weights=[pipe['weight'] for pipe in self.stock],
                       k=1)

        return Pipe(data[0])
