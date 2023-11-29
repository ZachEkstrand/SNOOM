import random
from sprite_object import *
from npc import *
from weapon import *
from projectile import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.sprite_positions = []
        self.npc_list = []
        self.del_queue = []
        self.npc_positions = {}
        self.npc_map_positions = {}
        self.restricted_area = [(self.game.player.x, self.game.player.y)]
        self.player_projectile_pos = {}
        self.enemy_projectile_pos = {}

        self.npc_num = self.game.player.room_num +4
        self.sprite_weights = [0.5, 1.0, 0.5]
        self.spawn_rate = 3.0

        self.key_pos = None

        self.place_objects()
        self.spawn_npc()

    def new_round(self):
        self.sprite_list = []
        self.sprite_positions = []
        self.npc_list = []
        self.del_queue = []
        self.npc_positions = {}
        self.npc_map_positions = {}
        self.player_projectile_pos = {}
        self.enemy_projectile_pos = {}
        self.npc_num = self.game.player.room_num +4
        self.sprite_weights[0] = self.game.player.room_num ** -0.9
        self.sprite_weights[1] = self.game.player.room_num ** 1.1
        self.sprite_weights[2] = self.game.player.room_num ** -0.2
        if self.spawn_rate < 50:
            self.spawn_rate += 0.5
        self.key_pos = None
        del self.weapon
        if self.game.player.room_num % 5 == 0:
            self.sprite_weights[0] = 0.5
            self.sprite_weights[1] = 1.0
            self.sprite_weights[2] = 0.5

        self.place_objects()
        self.spawn_npc()

    def place_objects(self):
        self.weapon = Weapon(self.game)
        #generate sprite objects
        for pos in self.game.map.space_indexes:
            if pos in self.restricted_area:
                continue
            create_sprite = random.choices([True, False], [self.spawn_rate, 100 -self.spawn_rate])[0]
            if create_sprite:
                random_sprite = random.choices([CandyCane, Tree, Snowpile], self.sprite_weights)[0]
                center_pos = (pos[0] +0.5, pos[1] +0.5)
                self.add_sprite(random_sprite(self.game, pos=center_pos))
                self.sprite_positions.append(pos)
        #place power cane
        pos = random.choice(self.game.map.space_indexes)
        while pos in self.sprite_positions:
            pos = random.choice(self.game.map.space_indexes)
        center_pos = (pos[0] +0.5, pos[1] +0.5)
        self.add_sprite(PowerCane(self.game, pos=center_pos))
        self.sprite_positions.append(pos)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    def spawn_projectile(self, pos, entity, angle, damage, powerup):
        if entity == self.game.player:
            self.add_sprite(Projectile(self.game, pos=pos, entity=entity, angle=angle, damage=damage, powerup=powerup))
        elif isinstance(entity, Boss):
            self.add_sprite(Projectile(self.game, pos=pos, shift=0, entity=entity, angle=angle, damage=damage, powerup=powerup))
        elif isinstance(entity, NPC):
            self.add_sprite(Projectile(self.game, pos=pos, shift=1, entity=entity, angle=angle, damage=damage, powerup=powerup))
    
    def spawn_key(self, pos):
        self.add_sprite(Key(self.game, pos=pos))
        self.key_pos = pos
        
    def spawn_npc(self):
        if self.game.player.room_num % 5 == 0:
            num_bosses = self.game.player.room_num / 5
            for i in range(int(num_bosses)):
                pos = random.choice(self.game.map.space_indexes)
                x, y = pos
                boss_address = self.add_npc(Boss(self.game, pos=(x +0.6, y +0.6)))
                boss_address.get_sprite()
                while boss_address.ray_cast_player_npc():
                    boss_address.destination = None
                    pos = random.choice(self.game.map.space_indexes)
                    x, y = pos
                    boss_address.x = x +0.6
                    boss_address.y = y +0.6
                    boss_address.get_sprite()
        else:
            for i in range(int(self.npc_num)):
                npc = NPC
                pos = random.choice(self.game.map.space_indexes)
                x, y = pos
                npc_address = self.add_npc(npc(self.game, pos=(x +0.6, y +0.6)))
                npc_address.get_sprite()
                while npc_address.ray_cast_player_npc():
                    npc_address.destination = None
                    pos = random.choice(self.game.map.space_indexes)
                    x, y = pos
                    npc_address.x = x +0.6
                    npc_address.y = y +0.6
                    npc_address.get_sprite()

        self.npc_positions = {npc:npc.pos for npc in self.npc_list}
        self.npc_map_positions = {npc:npc.map_pos for npc in self.npc_list}

    def add_npc(self, npc):
        self.npc_list.append(npc)
        return npc

    def update(self):
        self.check_ammo()

        self.npc_positions = {npc:npc.pos for npc in self.npc_list if npc.alive}
        self.npc_map_positions = {npc:npc.map_pos for npc in self.npc_list if npc.alive}
        self.sprite_positions = [sprite.pos for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]
        self.weapon.update()
        [sprite.update() for sprite in self.sprite_list]

        self.del_dead_objects()
        
    def del_dead_objects(self):
        for sprite in self.del_queue:
            self.sprite_list.remove(sprite)
    
    def check_ammo(self):
        snowpile_count = len([sprite for sprite in self.sprite_list if isinstance(sprite, Snowpile)])
        if self.game.player.ammo == 0 and snowpile_count < 2:
            self.respawn_snowpiles()

    def respawn_snowpiles(self):
        for i in range(4):
            random_pos = random.choice(self.game.map.space_indexes)
            while random_pos in self.sprite_positions:
                random_pos = random.choice(self.game.map.space_indexes)
            pos = (random_pos[0] +0.5, random_pos[1] +0.5)
            self.add_sprite(Snowpile(self.game, pos=pos))
            self.sprite_positions.append(random_pos)