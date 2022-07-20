from pygame import image as pgimage


class Arrow:
    def __init__(self):
        self.image = pgimage.load('./images/arrow.png')
        self.rect = self.image.get_rect()
        self.rect.topright = (240, 478)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def anim(self):
        if self.rect.right > 210:
            self.rect.move_ip(-1, 0)
        else:
            self.rect.right = 235
