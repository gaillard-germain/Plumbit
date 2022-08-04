from random import randint, choice

from config import tile_size, board_tile_x, board_tile_y


class Circuit:
    def __init__(self, factory):
        self.factory = factory
        self.grid = {}

        for y in range(board_tile_y):
            for x in range(board_tile_x):
                self.grid[(x*tile_size, y*tile_size)] = None

    def add(self, pipe):
        """ Add a pipe to the grid """

        self.grid[pipe.rect.topleft] = pipe

    def delete(self, pos):
        """ Delete a pipe from the grid """

        self.grid[pos] = None

    def rotate(self, pos, coef):
        """ Rotate a pipe in the grid """

        self.grid[pos].rotate(coef)

    def clear(self):
        """ Clear the grid dict """

        for pos in self.grid.keys():
            self.grid[pos] = None

    def get_nexts(self, pos):
        """ Util method for generating a ghost path to the end """

        for i in (-tile_size, tile_size):
            x = (pos[0]+i, pos[1])
            if x in self.grid.keys() and self.grid[x] is None:
                yield x
            y = (pos[0], pos[1]+i)
            if y in self.grid.keys() and self.grid[y] is None:
                yield y

    def get_free(self):
        """ Get the list of free positions """

        for pos, pipe in self.grid.items():
            if pipe is None:
                yield pos

    def get_locked(self):
        """ Get the list of the locked pipes """

        for pipe in self.grid.values():
            if pipe and pipe.locked:
                yield pipe.rect.topleft

    def is_locked(self, pos):
        """ Checks if the position is locked """

        if pos in self.get_locked():
            return True

    def is_mutable(self, pos):
        """ Checks if the pipe at this position is mutable """

        if self.grid[pos] and not self.grid[pos].immutable:
            return True

    def strew(self, valve, end, lvl):
        """ Strew valve, end and several blocks on the game board """

        self.clear()

        pos = (randint(1, board_tile_x-2) * tile_size,
               randint(1, board_tile_y-2) * tile_size)

        self.grid[pos] = '#'
        valve.rect.topleft = choice(list(self.get_nexts(pos)))
        self.grid[valve.rect.topleft] = valve
        valve.align(pos)

        for _ in range(5 + lvl*2):
            nexts = list(self.get_nexts(pos))
            if nexts:
                prev = pos
                pos = choice(nexts)
                self.grid[pos] = '#'
            else:
                break

        end.rect.topleft = pos
        self.grid[pos] = end
        end.align(prev)

        for i in range(randint(lvl, lvl+1)):
            block = self.factory.get_block()
            block.randomize_image()

            free = list(self.get_free())

            if free:
                block.rect.topleft = choice(free)
                self.grid[block.rect.topleft] = block
            else:
                break

        for pos, pipe in self.grid.items():
            if pipe == '#':
                self.grid[pos] = None

    def draw(self, surface):
        """ draw all the pipe in the grid """

        for pipe in self.grid.values():
            if pipe:
                pipe.draw(surface)
