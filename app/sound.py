from pygame import mixer


class Sound:
    def __init__(self):
        mixer.music.load('./sounds/music.ogg')

        self.put = mixer.Sound('./sounds/put.ogg')
        self.tic = mixer.Sound('./sounds/tic.ogg')
        self.sub = mixer.Sound('./sounds/sub.ogg')
        self.loose = mixer.Sound('./sounds/loose.ogg')
        self.win = mixer.Sound('./sounds/win.ogg')

        mixer.music.set_volume(0.4)
