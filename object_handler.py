import random
from sprite_object import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.del_queue = []
        self.place_objects()

    def place_objects(self):
        for pos in self.game.map.space_indexes:
            pos = (pos[0] +0.5, pos[1] +0.5)
            create_object = random.choices([True, False], [3, 97])[0]
            if create_object:
                random_sprite = random.choices([Decoration, Tree, Snowpile])[0]
                self.add_sprite(random_sprite(self.game, pos=pos))

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def update(self):
        del_indexes = []
        for i, sprite in enumerate(self.sprite_list):
            if sprite in self.del_queue:
                del_indexes.append(i)
            else:
                sprite.update()
        for i in del_indexes:
            del self.sprite_list[i]