from pygame import image as pgimage, mouse


class Cursor:
    """ A Cursor """

    def __init__(self, offset):
        self.images = [
            pgimage.load('./images/pointer.png'),
            pgimage.load('./images/locked.png')
        ]
        self.pin = 0
        self.rect = self.images[0].get_rect()

        self.offset = offset

    def process(self, is_locked):
        """ Move the cursor in the board """

        mouse_pos = mouse.get_pos()

        x = mouse_pos[0] - self.offset[0]
        y = mouse_pos[1] - self.offset[1]
        self.rect.topleft = (x-x % self.rect.width, y-y % self.rect.height)

        if is_locked(self.rect.topleft):
            self.pin = 1
        else:
            self.pin = 0

    def draw(self, surface):
        """ Blit the cursor on a surface """
        surface.blit(self.images[self.pin], self.rect.topleft)
