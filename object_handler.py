import random
from sprite_object import *
from npc import *
from weapon import *
from projectile import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.restricted_area = [(self.game.player.x, self.game.player.y)]
        self.sprite_list = {}
        self.npc_list = {}

        self.npc_num = self.game.player.room_num +4
        self.sprite_weights = [0.5, 1.0, 0.5]
        self.spawn_rate = 3.0

        self.key = []

        self.place_objects()
        self.spawn_npc()

    def new_round(self):
        self.sprite_list = {}
        self.npc_list = {}

        self.npc_num = self.game.player.room_num +4
        self.sprite_weights[0] = self.game.player.room_num ** -0.9
        self.sprite_weights[1] = self.game.player.room_num ** 1.1
        self.sprite_weights[2] = self.game.player.room_num ** -0.2
        if self.spawn_rate < 50:
            self.spawn_rate += 0.5

        self.key = []

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
        #place power cane
        pos = random.choice(self.game.map.space_indexes)
        while pos in self.sprite_list.values():
            pos = random.choice(self.game.map.space_indexes)
        center_pos = (pos[0] +0.5, pos[1] +0.5)
        self.add_sprite(PowerCane(self.game, pos=center_pos))

    def add_sprite(self, sprite):
        self.sprite_list[sprite] = sprite.pos

    def spawn_key(self, pos):
        self.key.append(Key(self.game, pos=pos))

    def spawn_projectile(self, pos, entity, angle, damage, powerup):
        if entity == self.game.player:
            self.add_sprite(Projectile(self.game, pos=pos, entity=entity, angle=angle, damage=damage, powerup=powerup))
        elif isinstance(entity, Boss):
            self.add_sprite(Projectile(self.game, pos=pos, shift=0, entity=entity, angle=angle, damage=damage, powerup=powerup))
        elif isinstance(entity, NPC):
            self.add_sprite(Projectile(self.game, pos=pos, shift=1, entity=entity, angle=angle, damage=damage, powerup=powerup))
        
    def spawn_npc(self):
        if self.game.player.room_num % 5 == 0:
            self.game.sound_manager.queue(9)
            self.game.sound_manager.fade_music()
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
            if self.game.sound_manager.get_track() == self.game.sound_manager.tracks[9]:
                self.game.sound_manager.queue(random.randint(0, 8))
                self.game.sound_manager.fade_music()
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

    def add_npc(self, npc):
        self.npc_list[npc] = npc.pos
        return npc

    def update(self):
        self.npc_list = {npc:npc.pos for npc in self.npc_list if npc.alive}
        [npc.update() for npc in self.npc_list]
        self.weapon.update()
        self.sprite_list = {sprite:sprite.pos for sprite in self.sprite_list if sprite.alive}
        [sprite.update() for sprite in self.sprite_list]
        [key.update() for key in self.key if key.alive]
        self.check_ammo()
    
    def check_ammo(self):
        snowpile_count = len([sprite for sprite in self.sprite_list if isinstance(sprite, Snowpile)])
        if self.game.player.ammo == 0 and snowpile_count < 2:
            self.respawn_snowpiles()

    def respawn_snowpiles(self):
        map_positions = [sprite.map_pos for sprite in self.sprite_list.keys()]
        for i in range(4):
            random_pos = random.choice(self.game.map.space_indexes)
            while random_pos in map_positions:
                random_pos = random.choice(self.game.map.space_indexes)
            pos = (random_pos[0] +0.5, random_pos[1] +0.5)
            self.add_sprite(Snowpile(self.game, pos=pos))