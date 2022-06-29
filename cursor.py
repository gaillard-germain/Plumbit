from pygame import image as pgimage


class Cursor:
    def __init__(self):
        self.pointer_image = pgimage.load('images/pointer.png')
        self.locked_image = pgimage.load('images/locked.png')

        self.image = self.pointer_image
        self.rect = self.image.get_rect()

    def confine(self, board, mouse_pos):
        """Maitien le curseur dans une zone definie"""

        x = mouse_pos[0] - board.left
        y = mouse_pos[1] - board.top
        self.rect.topleft = (x-x % 60, y-y % 60)
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > board.width:
            self.rect.right = board.width
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > board.height:
            self.rect.bottom = board.height
        return self.rect.topleft

    def hover_locked(self, circuit):
        if circuit.is_locked(self.rect.topleft):
            self.image = self.locked_image
        else:
            self.image = self.pointer_image

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
