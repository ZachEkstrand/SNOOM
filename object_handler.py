import random
from sprite_object import *
from npc import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.del_queue = []
        self.npc_positions = {}

        self.npc_num = 20
        self.npc_types = [NPC]
        self.weights = [100]

        self.place_objects()
        self.spawn_npc()

    def place_objects(self):
        for pos in self.game.map.space_indexes:
            pos = (pos[0] +0.5, pos[1] +0.5)
            create_object = random.choices([True, False], [3, 97])[0]
            if create_object:
                random_sprite = random.choices([Decoration, Tree, Snowpile])[0]
                self.add_sprite(random_sprite(self.game, pos=pos))

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
        
    def spawn_npc(self):
        for i in range(self.npc_num):
            npc = random.choices(self.npc_types, self.weights)[0]
            x, y = random.choice(self.game.map.space_indexes)
            self.add_npc(npc(self.game, pos=(x +0.6, y +0.6)))
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def update(self):
        del_indexes = []
        for i, sprite in enumerate(self.sprite_list):
            if sprite in self.del_queue:
                del_indexes.append(i)
            else:
                sprite.update()
        for i in del_indexes:
            del self.sprite_list[i]
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [npc.update() for npc in self.npc_list]