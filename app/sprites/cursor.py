from pygame import image as pgimage, mouse


class Cursor:
    """ A Cursor """

    def __init__(self, offset, is_locked):
        self.images = {
            'drop': pgimage.load('./images/drop.png').convert_alpha(),
            'locked': pgimage.load('./images/locked.png').convert_alpha(),
            'rotate': pgimage.load('./images/rotate.png').convert_alpha(),
            'delete': pgimage.load('./images/delete.png').convert_alpha(),
            'time': pgimage.load('./images/time.png').convert_alpha()
        }
        self.pin = 'drop'
        self.rect = self.images['drop'].get_rect()
        self.offset = offset
        self.is_locked = is_locked

    def process(self, pipe):
        """ Move the cursor on the board """

        mouse_pos = mouse.get_pos()

        x = mouse_pos[0] - self.offset[0]
        y = mouse_pos[1] - self.offset[1]
        self.rect.topleft = (x-x % self.rect.width, y-y % self.rect.height)

        if pipe.name == 'stopwatch':
            self.pin = 'time'
        elif pipe.name == 'bomb':
            self.pin = 'delete'
        elif pipe.name == 'wrench':
            self.pin = 'rotate'
        elif self.is_locked(self.rect.topleft):
            self.pin = 'locked'
        else:
            self.pin = 'drop'

    def draw(self, surface):
        """ Blit the cursor on a surface """
        surface.blit(self.images[self.pin], self.rect.topleft)
