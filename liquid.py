from pygame import image as pgimage


class Liquid:
    def __init__(self, valve, end, update_gain):
        self.image = pgimage.load('images/liquid.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = valve.rect.topleft
        self.previous = valve
        self.end = end
        self.path = (0, 0)
        self.update_gain = update_gain

    def check(self, circuit):
        """ Returns the next floodable pipe """

        eligibles = []

        for pipe in circuit:
            if (pipe.rect.topleft in self.previous.open_to()
                    and self.previous.rect.topleft in pipe.open_to()):
                if self.previous.name != 'cross':
                    return pipe

                else:
                    eligibles.append(pipe)

        for pipe in eligibles:
            if pipe.rect.topleft == (self.previous.rect.left+self.path[0],
                                     self.previous.rect.top+self.path[1]):
                return pipe

    def flood(self, circuit, bonus):
        """ Floods the circuit """

        pipe = self.check(circuit)

        if pipe:
            self.path = (pipe.rect.left - self.previous.rect.left,
                         pipe.rect.top - self.previous.rect.top)
            self.rect.move_ip(int(self.path[0]/pipe.rect.width)*2,
                              int(self.path[1]/pipe.rect.height)*2)

            if self.end.rect.contains(self.rect):
                gain = self.end.gain + bonus * 10
                self.update_gain(self.end.rect.topleft, gain)
                return 'WIN'

            elif pipe.rect.contains(self.rect):
                pipe.clog(self.path)
                self.previous = pipe
                if pipe.name == 'cross' and pipe.flooded:
                    pipe.gain = 200
                pipe.flooded = True
                self.update_gain(pipe.rect.topleft, pipe.gain)

        else:
            return 'LOOSE'

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
