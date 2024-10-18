from pygame import font as pgfont
from app.config import colors, font_default


class Stamp:
    def __init__(self, txt, size=10, color='black', pos=(0, 0),
                 alignment='center', font_path=font_default):
        self.txt = str(txt)
        self.size = size
        self.color = colors[color]
        self.pos = pos
        self.alignment = alignment
        self.font_path = font_path

        self.font = pgfont.Font(self.font_path, self.size)
        self.img = self.font.render(self.txt, True, self.color)
        self.rect = self.img.get_rect()

        self.align()

    def align(self):
        if self.alignment == 'center':
            self.rect.center = self.pos
        elif self.alignment == 'left':
            self.rect.midleft = self.pos
        elif self.alignment == 'right':
            self.rect.midright = self.pos

    def set_txt(self, txt, size=None, color=None, pos=None, alignment=None):
        """ Reset the stamp text and align it in terms of its bulk """

        self.txt = str(txt)

        if size:
            self.size = size
            self.font = pgfont.Font(self.font_path, self.size)

        if color:
            self.color = colors[color]

        if pos:
            self.pos = pos

        if alignment:
            self.alignment = alignment

        self.img = self.font.render(self.txt, True, self.color)
        self.rect = self.img.get_rect()

        self.align()

    def draw(self, surface):
        """ Draw stamp on the given surface """

        surface.blit(self.img, self.rect.topleft)

    def fly(self, max_height, delta):
        """ Makes the stamp floating up """

        if self.rect.top >= max_height:
            self.rect.move_ip(0, -delta)
        else:
            self.img.fill((0, 0, 0, 0))

    def swell(self, max_size, delta, pos=None):
        """ Makes the stamp swelling up """

        if self.size <= max_size:
            self.set_txt(self.txt, size=self.size+delta, pos=pos)
