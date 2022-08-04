from config import pipe_in_queue


class Box:
    def __init__(self, factory):
        self.factory = factory
        self.queue = []

    def fill(self):
        """ Refill the pipe's box """

        if self.queue:
            self.queue.clear()

        for i in range(pipe_in_queue):
            pipe = self.factory.get_random()
            pipe.rect.topleft = (250, 460 + i * 80)
            self.queue.append(pipe)

    def get_current(self):
        """ return the pipe of the top of the pile """

        return self.queue[0]

    def pickup(self):
        """ Pickup the first pipe in the box
            and add a new random one in the queue """

        picked = self.queue.pop(0)
        self.queue.append(self.factory.get_random())
        for i, pipe in enumerate(self.queue):
            pipe.rect.topleft = (250, 460 + i * 80)

        return picked

    def draw(self, surface):
        """ Draw all pipes in the queue """

        for pipe in self.queue:
            pipe.draw(surface)
