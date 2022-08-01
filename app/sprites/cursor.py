from pygame import image as pgimage, mouse


class Cursor:
    """ A Cursor """

    def __init__(self, offset):
        self.images = {
            'drop': pgimage.load('./images/drop.png'),
            'locked': pgimage.load('./images/locked.png'),
            'rotate': pgimage.load('./images/rotate.png')
        }
        self.pin = 'drop'
        self.rect = self.images['drop'].get_rect()

        self.offset = offset

    def process(self, is_locked, pipe):
        """ Move the cursor on the board """

        mouse_pos = mouse.get_pos()

        x = mouse_pos[0] - self.offset[0]
        y = mouse_pos[1] - self.offset[1]
        self.rect.topleft = (x-x % self.rect.width, y-y % self.rect.height)

        if is_locked(self.rect.topleft):
            self.pin = 'locked'
        elif pipe.name == 'wrench':
            self.pin = 'rotate'
        else:
            self.pin = 'drop'

    def draw(self, surface):
        """ Blit the cursor on a surface """
        surface.blit(self.images[self.pin], self.rect.topleft)
