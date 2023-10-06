import pygame as pg

audio = pg.mixer.Sound
path = 'resources/sound/'
class SoundHandler:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.master_volume = 0.5
        self.wind = False

        self.tracks = [
            audio(path +'tracks/8-bits_of_christmas.mp3'),             # 0
            audio(path +'tracks/angels_we_have_heard_underwater.mp3'), # 1
            audio(path +'tracks/dawn_of_the_final_day.mp3'),           # 2
            audio(path +'tracks/deck_the_castle_walls.mp3'),           # 3
            audio(path +'tracks/the_end.mp3'),                         # 4
            audio(path +'tracks/the_legend_of_santa.mp3'),             # 5
            audio(path +'tracks/unskippable_cutscene.mp3'),            # 6
        ]

        self.sfx = [
            audio(path +'sfx/start.mp3'), # 0
            audio(path +'sfx/wind.mp3'),  # 1 
            audio(path +'sfx/click.mp3'), # 2
            audio(path +'sfx/select.mp3') # 3
        ]
    
        self.set_master()

    def set_master(self):
        for sound in self.tracks:
            sound.set_volume(self.master_volume)
        for sound in self.sfx:
            sound.set_volume(self.master_volume)

    def play(self, index, sfx=True, loops=0, fade_ms=0):
        if sfx:
            if index == 1:
                self.wind = True
            audio.play(self.sfx[index], loops=loops, fade_ms=fade_ms)
        else:
            audio.play(self.tracks[index], loops=loops, fade_ms=fade_ms)

    def fade(self, index, sfx=True, time=500):
        if sfx:
            if index == 1:
                self.wind = False
            audio.fadeout(self.sfx[index], time)
        else:
            audio.fadeout(self.tracks[index, time])

    def set_volume(self, index, volume, sfx=True):
        volume = volume * self.master_volume
        if sfx:
            audio.set_volume(self.sfx[index], volume)
        else:
            audio.set_volume(self.tracks[index], volume)
