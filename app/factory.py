from pygame import image as pgimage
from random import choices
from sprites.pipe import Pipe


class Factory:
    def __init__(self):
        self.stock = [
            {
                'images': [pgimage.load('./images/golden_cross.png')],
                'apertures': [1, 1, 1, 1],
                'name': 'cross',
                'cost': -75,
                'gain': 100,
                'modifier': 2,
                'locked': True,
                'flooded': False,
                'weight': 1
            },
            {
                'images': [pgimage.load('./images/bomb.png')],
                'apertures': [],
                'name': 'bomb',
                'cost': 0,
                'gain': 0,
                'modifier': 0,
                'locked': False,
                'flooded': False,
                'weight': 12
            },
            {
                'images': [pgimage.load('./images/wrench.png')],
                'apertures': [],
                'name': 'wrench',
                'cost': 0,
                'gain': 0,
                'modifier': 0,
                'locked': False,
                'flooded': False,
                'weight': 15
            },
            {
                'images': [pgimage.load('./images/cross.png')],
                'apertures': [1, 1, 1, 1],
                'name': 'cross',
                'cost': -75,
                'gain': 100,
                'modifier': 0,
                'locked': False,
                'flooded': False,
                'weight': 40
            },
            {
                'images': [pgimage.load('./images/regular_tb.png')],
                'apertures': [0, 1, 0, 1],
                'name': 'straight',
                'cost': -50,
                'gain': 100,
                'modifier': 0,
                'locked': False,
                'flooded': False,
                'weight': 55
            },
            {
                'images': [pgimage.load('./images/regular_lr.png')],
                'apertures': [1, 0, 1, 0],
                'name': 'straight',
                'cost': -50,
                'gain': 100,
                'modifier': 0,
                'locked': False,
                'flooded': False,
                'weight': 55
            },
            {
                'images': [pgimage.load('./images/regular_tr.png')],
                'apertures': [0, 1, 1, 0],
                'name': 'elbow',
                'cost': -50,
                'gain': 100,
                'modifier': 0,
                'locked': False,
                'flooded': False,
                'weight': 50
            },
            {
                'images': [pgimage.load('./images/regular_tl.png')],
                'apertures': [1, 1, 0, 0],
                'name': 'elbow',
                'cost': -50,
                'gain': 100,
                'modifier': 0,
                'locked': False,
                'flooded': False,
                'weight': 50
            },
            {
                'images': [pgimage.load('./images/regular_br.png')],
                'apertures': [0, 0, 1, 1],
                'name': 'elbow',
                'cost': -50,
                'gain': 100,
                'modifier': 0,
                'locked': False,
                'flooded': False,
                'weight': 50
            },
            {
                'images': [pgimage.load('./images/regular_bl.png')],
                'apertures': [1, 0, 0, 1],
                'name': 'elbow',
                'cost': -50,
                'gain': 100,
                'modifier': 0,
                'locked': False,
                'flooded': False,
                'weight': 50
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
                'modifier': 0,
                'locked': True,
                'flooded': True
            },
            'end': {
                'images': [pgimage.load('./images/valve_2.png')],
                'apertures': [0, 0, 1, 0],
                'name': 'end',
                'cost': 0,
                'gain': 300,
                'modifier': 0,
                'locked': True,
                'flooded': True
            },
            'block': {
                'images': [
                    pgimage.load('./images/block.png'),
                    pgimage.load('./images/block2.png')
                ],
                'apertures': [0, 0, 0, 0],
                'name': 'block',
                'cost': 0,
                'gain': 0,
                'modifier': 0,
                'locked': True,
                'flooded': False
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
