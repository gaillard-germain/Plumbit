from pygame import image as pgimage
from random import choices

from sprites.pipe import Pipe
from sprites.block import Block
from sprites.tool import Tool


class Factory:
    def __init__(self):
        self.stock = [
            {
                'name': 'stopwatch',
                'images': [pgimage.load('./images/stopwatch.png')],
                'type': 'tool',
                'weight': 4
            },
            {
                'name': 'bomb',
                'images': [pgimage.load('./images/bomb.png')],
                'type': 'tool',
                'weight': 10
            },
            {
                'name': 'wrench',
                'images': [pgimage.load('./images/wrench.png')],
                'type': 'tool',
                'weight': 15
            },
            {
                'name': 'filter',
                'images': [pgimage.load('./images/filter.png')],
                'apertures': [1, 0, 1, 0],
                'cost': -100,
                'gain': 50,
                'modifier': 50,
                'locked': False,
                'immutable': False,
                'type': 'pipe',
                'weight': 4
            },
            {
                'name': 'cross',
                'images': [pgimage.load('./images/cross.png')],
                'apertures': [1, 1, 1, 1],
                'cost': -75,
                'gain': 100,
                'modifier': 0,
                'locked': False,
                'immutable': False,
                'type': 'pipe',
                'weight': 20
            },
            {
                'name': 'straight',
                'images': [pgimage.load('./images/straight.png')],
                'apertures': [1, 0, 1, 0],
                'cost': -50,
                'gain': 100,
                'modifier': 0,
                'locked': False,
                'immutable': False,
                'type': 'pipe',
                'weight': 60
            },
            {
                'name': 'elbow',
                'images': [pgimage.load('./images/elbow.png')],
                'apertures': [0, 0, 1, 1],
                'cost': -50,
                'gain': 100,
                'modifier': 0,
                'locked': False,
                'immutable': False,
                'type': 'pipe',
                'weight': 100
            },
        ]
        self.extra = {
            'valve': {
                'name': 'valve',
                'images': [
                    pgimage.load('./images/valve_1.png'),
                    pgimage.load('./images/valve_1a.png')
                ],
                'apertures': [0, 0, 1, 0],
                'cost': 0,
                'gain': 0,
                'modifier': 0,
                'locked': True,
                'immutable': True,
                'type': 'pipe'
            },
            'end': {
                'name': 'end',
                'images': [pgimage.load('./images/valve_2.png')],
                'apertures': [0, 0, 1, 0],
                'cost': 0,
                'gain': 300,
                'modifier': 0,
                'locked': True,
                'immutable': True,
                'type': 'pipe'
            },
            'block': {
                'name': 'block',
                'images': [
                    pgimage.load('./images/block.png'),
                    pgimage.load('./images/block2.png')
                ],
                'locked': True,
                'immutable': False,
                'type': 'block'
            }
        }

    def get_valve(self):
        """ Return a valve """

        return Pipe(self.extra['valve'])

    def get_end(self):
        """ Return an end """

        return Pipe(self.extra['end'])

    def get_block(self):
        """ Return a block """

        return Block(self.extra['block'])

    def get_random(self):
        """ Return a random pipe """

        data = choices(self.stock,
                       weights=[pipe['weight'] for pipe in self.stock],
                       k=1)[0]

        if data['type'] == 'pipe':
            pipe = Pipe(data)

            if pipe.name != 'cross':
                pipe.rotate()

            return pipe

        elif data['type'] == 'tool':
            return Tool(data)
