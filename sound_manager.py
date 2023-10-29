import pygame as pg

audio = pg.mixer.Sound
path = 'resources/sound/tracks/'
spath = 'resources/sound/sfx/'
class SoundManager:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        pg.mixer.set_num_channels(16)
        self.master_volume = 1

        self.tracks = [
            audio(path +'8-bits_of_christmas.mp3'),             # 0
            audio(path +'angels_we_have_heard_underwater.mp3'), # 1
            audio(path +'dawn_of_the_final_day.mp3'),           # 2
            audio(path +'deck_the_castle_walls.mp3'),           # 3
            audio(path +'the_legend_of_santa.mp3'),             # 4
            audio(path +'the_end.mp3'),                         # 5
            audio(path +'game_over.mp3')                        # 6
        ]

        self.sfx = [
            audio(spath +'wind.mp3'),           # 0
            audio(spath +'start.mp3'),          # 1 
            audio(spath +'click.mp3'),          # 2
            audio(spath +'select.mp3'),         # 3
            audio(spath +'throw.mp3'),          # 4
            audio(spath +'player_pain_1.mp3'),  # 5
            audio(spath +'player_pain_2.mp3'),  # 6
            audio(spath +'player_pain_3.mp3'),  # 7
            audio(spath +'enemy_pain_1.mp3'),   # 8
            audio(spath +'enemy_pain_2.mp3'),   # 9
            audio(spath +'enemy_pain_3.mp3'),   # 10
            audio(spath +'enemy_death.mp3'),    # 11
            audio(spath +'snow_pickup.wav'),    # 12
            audio(spath +'snowball_death.mp3'), # 13
            audio(spath +'key.wav'),            # 14
            audio(spath +'key_pickup.mp3'),     # 15
            audio(spath +'door.mp3'),           # 16
        ]
    
        self.set_master()

    def set_master(self):
        for sound in self.tracks:
            sound.set_volume(self.master_volume)
        for sound in self.sfx:
            sound.set_volume(self.master_volume)

    def play(self, sound_index, sfx=True, loops=0, fade_ms=0, player=False):
        channel_index = self.find_channel(sound_index, sfx, player)
        if sfx:
            pg.mixer.Channel(channel_index).play(self.sfx[sound_index], loops=loops, fade_ms=fade_ms)
        else:
            pg.mixer.Channel(channel_index).play(self.tracks[sound_index], loops=loops, fade_ms=fade_ms)

    def find_channel(self, index, sfx, player):
        if sfx == False:
            return 1
        
        if index == 0:
            return 0
        if index in [1, 2, 3]:
            return self.check_channel([2, 3])
        if index == 4:
            if player:
                return 4
            return self.check_channel([6, 7, 8, 9, 10])
        if index in [5, 6, 7]:
            return 5
        if index in [8, 9, 10, 12, 14]:
            return self.check_channel([11, 12])
        if index in [11, 15, 16]:
            return 15
        if index == 13:
            return self.check_channel([13, 14])
        
        
    def check_channel(self, nums):
        for i in nums:
            if not pg.mixer.Channel(i).get_busy():
                return i
        return nums[0]

    def fade(self, index, sfx=True, time=500):
        if sfx:
            if index == 1:
                self.wind = False
            audio.fadeout(self.sfx[index], time)
        else:
            audio.fadeout(self.tracks[index, time])

    def set_volume(self, index, volume):
        volume = volume * self.master_volume
        audio.set_volume(self.sfx[index], volume)

    def set_music_volume(self, volume):
        volume = volume * self.master_volume
        pg.mixer.Channel(1).set_volume(volume)

    def get_queue(self):
        return pg.mixer.Channel(1).get_queue()
        
    def queue(self, index):
        pg.mixer.Channel(1).queue(self.tracks[index])

    def pause(self):
        self.set_music_volume(0.3)
        for i in range(4, 16):
            pg.mixer.Channel(i).pause()

    def unpause(self):
        for i in range(4, 16):
            pg.mixer.Channel(i).unpause()
    
    def get_busy(self, index):
        return pg.mixer.Channel(index).get_busy()