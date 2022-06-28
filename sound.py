from pygame import mixer


class Sound:
    def __init__(self):
        mixer.pre_init(44100, -16, 2, 2048)
        mixer.init()

        self.music = mixer.Sound('son/Solve The Puzzle.ogg')
        self.put = mixer.Sound('son/put.ogg')
        self.tic = mixer.Sound('son/tic.ogg')
        self.sub = mixer.Sound('son/sub.ogg')
        self.loose = mixer.Sound('son/loose.ogg')
        self.win = mixer.Sound('son/win.ogg')

        self.music.set_volume(0.4)
