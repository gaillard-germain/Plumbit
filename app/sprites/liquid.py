from pygame import image as pgimage

from sprites.pipe import Pipe


class Liquid:
    def __init__(self):
        self.image = pgimage.load('./images/liquid.png')
        self.rect = self.image.get_rect()
        self.previous = None
        self.path = (0, 0)
        self.modifier = 1

    def reset(self, valve):
        self.previous = valve
        self.rect.topleft = valve.rect.topleft
        self.path = (0, 0)
        self.modifier = 1

    def check(self, circuit):
        """ Returns the next floodable pipe """

        eligibles = []

        for pos in self.previous.open_to():
            if pos not in circuit.keys():
                continue
            pipe = circuit[pos]
            if (isinstance(pipe, Pipe)
                    and self.previous.rect.topleft in pipe.open_to()):
                if self.previous.name != 'cross':
                    return pipe

                else:
                    eligibles.append(pipe)

        for pipe in eligibles:
            if pipe.rect.topleft == (self.previous.rect.left+self.path[0],
                                     self.previous.rect.top+self.path[1]):
                return pipe

    def flood(self, circuit):
        """ Floods the circuit """

        pipe = self.check(circuit)

        if pipe:
            self.path = (pipe.rect.left - self.previous.rect.left,
                         pipe.rect.top - self.previous.rect.top)
            self.rect.move_ip(int(self.path[0]/pipe.rect.width)*2,
                              int(self.path[1]/pipe.rect.height)*2)

            if pipe.rect.contains(self.rect):
                if pipe.modifier:
                    self.modifier *= pipe.modifier

                if pipe.name == 'cross' and pipe.locked:
                    pipe.gain *= 2

                pipe.clog(self.path)
                pipe.gain *= self.modifier
                pipe.immutable = True
                self.previous = pipe

                return pipe

            else:
                return 'flooding'

    def draw(self, surface):
        """ draw liquid """

        surface.blit(self.image, self.rect.topleft)
