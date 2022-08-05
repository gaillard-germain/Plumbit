from pygame import image as pgimage

from sprites.pipe import Pipe


class Liquid:
    def __init__(self):
        self.image = pgimage.load('./images/liquid.png')
        self.rect = self.image.get_rect()
        self.prev = None
        self.path = (0, 0)
        self.modifier = 1

    def reset(self, valve):
        """ Reset the Liquid position and modifier """

        self.prev = valve
        self.rect.topleft = valve.rect.topleft
        self.path = (0, 0)
        self.modifier = 1

    def check(self, circuit):
        """ Returns the next floodable pipe """

        for pos in self.prev.open_to():
            pipe = circuit[pos]
            if (isinstance(pipe, Pipe)
                    and self.prev.rect.topleft in pipe.open_to()):
                if self.prev.name != 'cross':
                    return pipe

                elif pipe.rect.topleft == (self.prev.rect.left+self.path[0],
                                           self.prev.rect.top+self.path[1]):
                    return pipe

    def flood(self, circuit):
        """ Floods the circuit """

        pipe = self.check(circuit)

        if pipe:
            self.path = (pipe.rect.left - self.prev.rect.left,
                         pipe.rect.top - self.prev.rect.top)
            self.rect.move_ip(int(self.path[0]/pipe.rect.width)*2,
                              int(self.path[1]/pipe.rect.height)*2)

            if pipe.rect.contains(self.rect):
                if pipe.modifier:
                    self.modifier += pipe.modifier

                if pipe.name == 'cross' and pipe.locked:
                    pipe.gain = 200

                if pipe.name != 'end':
                    pipe.clog(self.path)
                    pipe.gain *= self.modifier

                pipe.immutable = True
                self.prev = pipe

                return pipe

            else:
                return 'flooding'

    def draw(self, surface):
        """ draw liquid """

        surface.blit(self.image, self.rect.topleft)
