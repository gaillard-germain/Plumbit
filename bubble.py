from pygame import Surface, SRCALPHA

from tools import display_txt


class Bubble:
    def __init__(self, tile_size):
        self.layer = Surface((tile_size, tile_size), SRCALPHA, 32)
        self.rect = self.layer.get_rect()

    def process(self):
        if self.rect.top <= -20:
            self.layer.fill((255, 255, 255, 0))

    def update(self, pos, value):
        self.rect.topleft = pos
        self.layer.fill((255, 255, 255, 0))
        if int(value) > 0:
            txt = '+{} $'.format(value)
            color = (70, 170, 60)
        else:
            txt = '{} $'.format(value)
            color = (194, 69, 26)

        display_txt(txt, 26, color, self.layer)

    def draw(self, surface):
        surface.blit(self.layer, self.rect.topleft)

    def anim(self):
        if self.rect.top >= -20:
            self.rect.move_ip(0, -2)
