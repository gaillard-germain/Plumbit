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
                eligibles.append(pipe)

        if len(eligibles) > 1:
            for pipe in eligibles:
                if pipe.rect.topleft == (self.previous.rect.left+self.path[0],
                                         self.previous.rect.top+self.path[1]):
                    return pipe

        elif len(eligibles) == 1:
            return eligibles[0]

        else:
            return None

    def flood(self, circuit, bonus):
        """ Floods the circuit """

        pipe = self.check(circuit)

        if pipe:
            self.path = (pipe.rect.left - self.previous.rect.left,
                         pipe.rect.top - self.previous.rect.top)
            self.rect = self.rect.move(int(self.path[0]/60),
                                       int(self.path[1]/60))

            if self.rect.topleft == self.end.rect.topleft:
                gain = self.end.value + bonus * 10
                self.update_gain(self.end.rect.topleft, gain)
                return 'WIN'

            elif self.rect.topleft == pipe.rect.topleft:
                pipe.clog(self.path)
                self.previous = pipe
                self.update_gain(pipe.rect.topleft, pipe.value)

        else:
            return 'LOOSE'

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
