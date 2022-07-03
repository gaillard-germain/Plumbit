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


def display_txt(txt, size, color, surface, x='center', y='center'):
    """ Display text in the middle of a surface """

    txt = str(txt)
    font = pgfont.Font('fonts/Amatic-Bold.ttf', size)
    img_txt = font.render(txt, True, color)
    if x == 'center':
        x = int((surface.get_width() - font.size(txt)[0])/2)
    if y == 'center':
        y = int((surface.get_height() - font.size(txt)[1])/2)
    return surface.blit(img_txt, (x, y))


def load_json(data_file):
    """ Load a json file """

    with open(data_file) as data:
        return json.load(data)


def new_record(score):
    """ Check if the score could enter the TopTen """

    topten = load_json('topten.json')
    for index, player in enumerate(topten):
        if score > player["score"]:
            return index
    return None


def update_json(index, winner, score):
    """ Update the topten.json  file """

    topten = load_json('topten.json')
    topten.insert(index, dict(name=winner, score=score))
    if len(topten) > 10:
        del topten[-1]
    with open('topten.json', 'w') as file:
        json.dump(topten, file, indent=4)
    return 0
