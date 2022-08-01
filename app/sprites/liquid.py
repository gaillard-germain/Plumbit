from pygame import image as pgimage, time


class Liquid:
    def __init__(self, valve, end, circuit, update_gain, flood_event):
        self.image = pgimage.load('./images/liquid.png')
        self.rect = self.image.get_rect()
        self.valve = valve
        self.previous = None
        self.end = end
        self.circuit = circuit
        self.path = (0, 0)
        self.modifier = 1
        self.update_gain = update_gain
        self.FLOOD = flood_event

    def reset(self):
        self.previous = self.valve
        self.rect.topleft = self.valve.rect.topleft
        self.path = (0, 0)
        self.modifier = 1

    def check(self):
        """ Returns the next floodable pipe """

        eligibles = []

        for pos in self.previous.open_to():
            if pos not in self.circuit.keys():
                continue
            pipe = self.circuit[pos]
            if pipe and self.previous.rect.topleft in pipe.open_to():
                if self.previous.name != 'cross':
                    return pipe

                else:
                    eligibles.append(pipe)

        for pipe in eligibles:
            if pipe.rect.topleft == (self.previous.rect.left+self.path[0],
                                     self.previous.rect.top+self.path[1]):
                return pipe

    def flood(self, time_bonus):
        """ Floods the circuit """

        pipe = self.check()

        if pipe:
            self.path = (pipe.rect.left - self.previous.rect.left,
                         pipe.rect.top - self.previous.rect.top)
            self.rect.move_ip(int(self.path[0]/pipe.rect.width)*2,
                              int(self.path[1]/pipe.rect.height)*2)

            if self.end.rect.contains(self.rect):
                gain = self.end.gain * self.modifier + time_bonus * 10
                self.update_gain(self.end.rect.center, gain)
                return 'WIN'

            elif pipe.rect.contains(self.rect):
                pipe.clog(self.path)
                self.previous = pipe
                if pipe.name == 'cross' and pipe.flooded:
                    pipe.gain = 200
                pipe.flooded = True
                if pipe.modifier:
                    time.set_timer(self.FLOOD, 20)
                    self.modifier *= pipe.modifier
                self.update_gain(pipe.rect.center, pipe.gain * self.modifier)

        else:
            return 'LOOSE'

    def draw(self, surface):
        """ draw liquid """

        surface.blit(self.image, self.rect.topleft)
