from pygame import font as pgfont
from config import colors, font_default


class Stamp:
    def __init__(self, txt, size=10, color='black', pos=(0, 0),
                 align='center', font_path=font_default):
        self.txt = txt
        self.font_path = font_path
        self.size = size
        self.font = pgfont.Font(font_path, size)
        self.color = colors[color]
        self.pos = pos
        self.align = align

        self.set_txt(txt)

    def set_txt(self, txt, size=None, color=None, pos=None, align=None, ):
        """ Set or reset the stamp text and align it in terms of its bulk """

        self.txt = str(txt)

        if size:
            self.size = size
            self.font = pgfont.Font(self.font_path, self.size)

        if color:
            self.color = colors[color]

        self.img = self.font.render(self.txt, True, self.color)
        self.rect = self.img.get_rect()

        if pos:
            self.pos = pos

        if align:
            self.align = align

        if self.align == 'center':
            self.rect.center = self.pos
        elif self.align == 'left':
            self.rect.midleft = self.pos
        elif self.align == 'right':
            self.rect.midright = self.pos

    def draw(self, surface):
        """ Draw stamp on the given surface """

        surface.blit(self.img, self.rect.topleft)

    def fly(self, max_height):
        """ make the stamp floating up """

        if self.rect.top >= max_height:
            self.rect.move_ip(0, -3)
            self.swell(24, 1, self.rect.center)
        else:
            self.img.fill((0, 0, 0, 0))

    def swell(self, max_size, delta, pos=None):
        if self.size <= max_size:
            if pos:
                self.set_txt(self.txt, size=self.size+delta, pos=pos)
            else:
                self.set_txt(self.txt, size=self.size+delta)
