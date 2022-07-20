from pygame import image as pgimage


class Arrow:
    def __init__(self):
        self.image = pgimage.load('./images/arrow.png')
        self.rect = self.image.get_rect()
        self.start_pos = (200, 460)
        self.rect.topleft = self.start_pos

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def anim(self):
        if self.rect.left > 180:
            self.rect.move_ip(-1, 0)
        else:
            self.rect.left = self.start_pos[0]
