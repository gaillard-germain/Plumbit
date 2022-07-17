from pygame import image as pgimage, mouse


class Cursor:
    """ A Cursor """

    def __init__(self, offset):
        self.pointer_image = pgimage.load('images/pointer.png')
        self.locked_image = pgimage.load('images/locked.png')

        self.image = self.pointer_image
        self.rect = self.image.get_rect()

        self.offset = offset

    def process(self, is_locked):
        """ Move the cursor in the board """

        mouse_pos = mouse.get_pos()

        x = mouse_pos[0] - self.offset[0]
        y = mouse_pos[1] - self.offset[1]
        self.rect.topleft = (x-x % self.rect.width, y-y % self.rect.height)

        if is_locked(self.rect.topleft):
            self.image = self.locked_image
        else:
            self.image = self.pointer_image

    def draw(self, surface):
        """ Blit the cursor on a surface """
        surface.blit(self.image, self.rect.topleft)
