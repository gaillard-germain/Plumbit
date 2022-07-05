from pygame import mixer


class Sound:
    def __init__(self):
        mixer.music.load('son/music.ogg')

        self.put = mixer.Sound('son/put.ogg')
        self.tic = mixer.Sound('son/tic.ogg')
        self.sub = mixer.Sound('son/sub.ogg')
        self.loose = mixer.Sound('son/loose.ogg')
        self.win = mixer.Sound('son/win.ogg')

        mixer.music.set_volume(0.4)
