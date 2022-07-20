import os
import shutil
import json
from pygame import font as pgfont


def check_topten():
    """ Check if topten.json exists, if not copy it from a clean file """

    if not os.path.exists('topten.json'):
        path = os.getcwd()
        src = '{}/topten_clean.json'.format(path)
        dst = '{}/topten.json'.format(path)

        shutil.copyfile(src, dst)


def display_txt(txt, size, color, surface, x=None, y=None, justify='center'):
    """ Display text in the middle of a surface """

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


def load_topten():
    """ Load a json file """

    with open('./topten.json') as data:
        return json.load(data)


def new_record(score):
    """ Check if the score could enter the TopTen """

    topten = load_topten()
    for index, player in enumerate(topten):
        if score > player["score"]:
            return index
    return None


def update_topten(index, winner, score):
    """ Update the topten.json  file """

    topten = load_topten()
    topten.insert(index, dict(name=winner, score=score))
    if len(topten) > 10:
        del topten[-1]
    with open('topten.json', 'w') as file:
        json.dump(topten, file, indent=4)
    return 0
