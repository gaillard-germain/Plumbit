from pygame import image as pgimage
from random import choices
from sprites.pipe import Pipe


class Factory:
    def __init__(self):
        self.stock = [
            {
                'images': [pgimage.load('./images/cross.png')],
                'apertures': [1, 1, 1, 1],
                'name': 'cross',
                'cost': -75,
                'gain': 100,
                'locked': False,
                'weight': 30
            },
            {
                'images': [pgimage.load('./images/regular_tb.png')],
                'apertures': [0, 1, 0, 1],
                'name': 'straight',
                'cost': -50,
                'gain': 100,
                'locked': False,
                'weight': 50
            },
            {
                'images': [pgimage.load('./images/regular_lr.png')],
                'apertures': [1, 0, 1, 0],
                'name': 'straight',
                'cost': -50,
                'gain': 100,
                'locked': False,
                'weight': 50
            },
            {
                'images': [pgimage.load('./images/regular_tr.png')],
                'apertures': [0, 1, 1, 0],
                'name': 'elbow',
                'cost': -50,
                'gain': 100,
                'locked': False,
                'weight': 40
            },
            {
                'images': [pgimage.load('./images/regular_tl.png')],
                'apertures': [1, 1, 0, 0],
                'name': 'elbow',
                'cost': -50,
                'gain': 100,
                'locked': False,
                'weight': 40
            },
            {
                'images': [pgimage.load('./images/regular_br.png')],
                'apertures': [0, 0, 1, 1],
                'name': 'elbow',
                'cost': -50,
                'gain': 100,
                'locked': False,
                'weight': 40
            },
            {
                'images': [pgimage.load('./images/regular_bl.png')],
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
                'images': [
                    pgimage.load('./images/valve_1.png'),
                    pgimage.load('./images/valve_1a.png')
                ],
                'apertures': [0, 0, 1, 0],
                'name': 'valve',
                'cost': 0,
                'gain': 0,
                'locked': True,
            },
            'end': {
                'images': [pgimage.load('./images/valve_2.png')],
                'apertures': [0, 0, 1, 0],
                'name': 'end',
                'cost': 0,
                'gain': 300,
                'locked': True,
            },
            'block': {
                'images': [
                    pgimage.load('./images/block.png'),
                    pgimage.load('./images/block2.png')
                ],
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
