import random
from sprite_object import *
from npc import *
from weapon import *
from projectile import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.del_queue = []
        self.npc_positions = {}
        self.restricted_area = [(i, j) for i in range(int(self.game.player.x), int(self.game.player.x) +2) for j in range(int(self.game.player.y) -1, int(self.game.player.y) +2)]
        self.player_projectile_pos = {}

        self.npc_num = 10
        self.npc_types = [NPC]
        self.weights = [100]

        self.place_objects()
        self.spawn_npc()

    def place_objects(self):
        self.weapon = Weapon(self.game)
        for pos in self.game.map.space_indexes:
            if pos in self.restricted_area:
                continue
            pos = (pos[0] +0.5, pos[1] +0.5)
            create_object = random.choices([True, False], [3, 97])[0]
            if create_object:
                random_sprite = random.choices([Decoration, Tree, Snowpile])[0]
                self.add_sprite(random_sprite(self.game, pos=pos))

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def spawn_projectile(self, pos, entity, angle):
        if entity == 'player':
            self.add_sprite(Projectile(self.game, pos=pos, angle=angle))
        
    def spawn_npc(self):
        for i in range(self.npc_num):
            npc = random.choices(self.npc_types, self.weights)[0]
            pos = random.choice(self.game.map.space_indexes)
            while pos in self.restricted_area:
                pos = random.choice(self.game.map.space_indexes)
            x, y = pos
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

        self.player_projectile_pos = {snowball:snowball.pos for snowball in self.sprite_list if isinstance(snowball, Projectile) and snowball.alive and snowball.entity == 'player'}
        #self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [npc.update() for npc in self.npc_list]
        self.weapon.update()