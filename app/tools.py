from pygame import font as pgfont


def display_txt(txt, size, color, surface, x=None, y=None, justify='center'):
    """ Place a text on a surface """

    txt = str(txt)
    font = pgfont.Font('./fonts/TheConfessionRegular-YBpv.ttf', size)
    img_txt = font.render(txt, True, color)
    txt_size = font.size(txt)
    if not x:
        x = surface.get_width()/2
    if not y:
        y = surface.get_height()/2 - txt_size[1]/2

    if justify == 'center':
        pos = (x - txt_size[0]/2, y)
    elif justify == 'left':
        pos = (x, y)
    elif justify == 'right':
        pos = (x - txt_size[0], y)

    return surface.blit(img_txt, pos)
