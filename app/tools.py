from pygame import font as pgfont


def display_txt(txt, size, color, surface, x=None, y=None, justify='center'):
    """ Place a text on a surface surface """

    txt = str(txt)
    font = pgfont.Font('./fonts/TheConfessionRegular-YBpv.ttf', size)
    img_txt = font.render(txt, True, color)
    txt_size = font.size(txt)
    if not x:
        x = surface.get_width()/2
    if not y:
        y = surface.get_height()/2

    if justify == 'center':
        pos = (x - txt_size[0]/2, y - txt_size[1]/2)
    elif justify == 'left':
        pos = (x, y - txt_size[1]/2)
    elif justify == 'right':
        pos = (x - txt_size[0], y - txt_size[1]/2)

    return surface.blit(img_txt, pos)
