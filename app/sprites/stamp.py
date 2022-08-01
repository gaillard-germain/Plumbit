from pygame import font as pgfont
from misc import colors


class Stamp:
    def __init__(self, txt, size, color='black', pos=(0, 0), align='center'):
        self.font = pgfont.Font('./fonts/TheConfessionRegular-YBpv.ttf', size)
        self.color = colors[color]
        self.pos = pos
        self.align = align

        self.set_txt(txt)

    def set_txt(self, txt, color='default', pos='default', align='default'):
        """ Set or reset the stamp text and align it in terms of its bulk """

        self.txt = str(txt)

        if color == 'default':
            color = self.color
        else:
            color = colors[color]

        self.img = self.font.render(self.txt, True, color)
        self.rect = self.img.get_rect()

        if pos == 'default':
            pos = self.pos

        if align == 'default':
            align = self.align

        if align == 'center':
            self.rect.center = pos
        elif align == 'left':
            self.rect.midleft = pos
        elif align == 'right':
            self.rect.midright = pos

    def draw(self, surface):
        """ Draw stamp """

        surface.blit(self.img, self.rect.topleft)

    def fly(self, max_y):
        """ make the stamp floating up """

        if self.rect.top >= max_y:
            self.rect.move_ip(0, -2)
        else:
            self.img.fill((255, 255, 255, 0))
