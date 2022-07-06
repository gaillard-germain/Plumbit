from pygame import image as pgimage


class Liquid:
    def __init__(self):
        self.image = pgimage.load('images/liquid.png')
        self.rect = self.image.get_rect()
        self.previous = None
        self.path = (0, 0)

    def set_up(self, valve):
        self.previous = valve
        self.rect.topleft = valve.rect.topleft
        self.path = (0, 0)

    def check(self, circuit):
        """ Returns the next floodable pipe """

        eligibles = []
        elected = None
        for pipe in circuit:
            if (pipe.rect.topleft in self.previous.open_to()
                    and self.previous.rect.topleft in pipe.open_to()):
                eligibles.append(pipe)
        for pipe in eligibles:
            if self.previous.name == 'regular':
                elected = pipe
            elif self.previous.name == 'cross':
                if pipe.rect.topleft == (self.previous.rect.left+self.path[0],
                                         self.previous.rect.top+self.path[1]):
                    elected = pipe
        return elected

    def flood(self, circuit, end):
        """ Floods the circuit """

        pipe = self.check(circuit)

        if pipe:
            self.path = (pipe.rect.left - self.previous.rect.left,
                         pipe.rect.top - self.previous.rect.top)
            self.rect = self.rect.move(int(self.path[0]/60),
                                       int(self.path[1]/60))

            if self.rect.topleft == end.rect.topleft:
                return ('WIN', end)

            elif self.rect.topleft == pipe.rect.topleft:
                pipe.clog(self.path)
                self.previous = pipe
                return ('RUNNING', pipe)

            else:
                return ('RUNNING', None)

        else:
            return ('LOOSE', None)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
