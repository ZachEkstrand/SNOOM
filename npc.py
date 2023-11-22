import random
from sprite_object import *

class NPC(AnimatedSprite): #elf cadet
    def __init__(self, game, path='resources/sprites/npc/elf/walk/7.png', pos=(1, 1),
                 scale=0.6, shift=0.38, animation_time=100):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.idle_image = pg.image.load('resources/sprites/npc/elf/walk/7.png').convert_alpha()
        self.death_images = self.get_images('resources/sprites/npc/elf/death')
        self.pain_images = self.get_images('resources/sprites/npc/elf/pain')
        self.walk_images = self.get_images('resources/sprites/npc/elf/walk')

        self.attack_dist = random.randint(3, 6)
        self.point_give = round(self.attack_dist * 3, -1)
        self.attack_delay = 180
        self.speed = 0.001
        self.size = 15
        self.hitbox = self.size / 70
        self.health = 100
        self.attack_damage = 5
        self.last_attack_time = 0
        self.attack_delay = 1000
        self.pain_frame_time = 80
        self.last_pain_frame = pg.time.get_ticks()
        self.death_frame_time = 40
        self.last_death_frame = pg.time.get_ticks()
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.pain_frame_counter = -1
        self.death_frame_counter = -1
        self.destination = None

    def update(self):
        if self.game.scene_manager.current_scene == 'pause_menu': pass 
        else: 
            self.check_animation_time()
            self.run_logic()

        self.get_sprite()

    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            if self.pain:
                self.animate_pain()
            elif self.ray_cast_value:
                if self.dist < self.attack_dist:
                    self.attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()
            elif self.destination:
                self.animate(self.walk_images)
                self.movement()
            else:
                self.image = self.idle_image
        else:
            self.animate_death()

    def ray_cast_player_npc(self):
        if self.game.player.map_pos == self.map_pos:
            return True

        wall_dist_v, wall_dist_h = 0, 0
        player_dist_v, player_dist_h = 0, 0

        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.theta

        sin_a = math.sin(ray_angle)
        cos_a = math.cos(ray_angle)

        # horizontals
        y_hor, dy = (y_map +1, 1) if sin_a > 0 else (y_map -1e-6, -1)

        depth_hor = (y_hor -oy) / sin_a
        x_hor = ox +depth_hor * cos_a

        delta_depth = dy / sin_a
        dx = delta_depth * cos_a

        for i in range(MAX_DEPTH):
            tile_hor = int(x_hor), int(y_hor)
            if tile_hor == self.map_pos:
                player_dist_h = depth_hor
                break
            if tile_hor in self.game.map.map_diction:
                wall_dist_h = depth_hor
                break
            x_hor += dx
            y_hor += dy
            depth_hor += delta_depth

        # verticals
        x_vert, dx = (x_map +1, 1) if cos_a > 0 else (x_map -1e-6, -1)

        depth_vert = (x_vert -ox) / cos_a
        y_vert = oy +depth_vert * sin_a

        delta_depth = dx / cos_a
        dy = delta_depth * sin_a

        for i in range(MAX_DEPTH):
            tile_vert = int(x_vert), int(y_vert)
            if tile_vert == self.map_pos:
                player_dist_v = depth_vert
                break
            if tile_vert in self.game.map.map_diction:
                wall_dist_v = depth_vert
                break
            x_vert += dx
            y_vert += dy
            depth_vert += delta_depth

        player_dist = max(player_dist_v, player_dist_h)
        wall_dist = max(wall_dist_v, wall_dist_h)

        if 0 < player_dist < wall_dist or not wall_dist:
            self.destination = self.player.map_pos
            return True
        return False
    
    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def take_damage(self, damage, powerup):
        self.pain = True
        self.health -= damage
        self.player.hit_streak += 1
        if powerup == 'STUN':
            self.pain_frame_time = 500
        self.check_health()

    def check_health(self):
        if self.health < 1:
            self.game.sound_manager.play(11)
            self.alive = False
            self.player.kill_streak += 1
            self.game.player.score += self.point_give +self.player.kill_streak * self.player.room_num +self.player.hit_streak * self.player.room_num
            if len([npc for npc in self.game.object_handler.npc_list if npc.alive]) == 0:
                self.game.object_handler.spawn_key(self.pos)
        else:
            self.game.sound_manager.play(random.randint(8, 10))

    def animate_pain(self):
        time_now = pg.time.get_ticks()
        if self.pain_frame_counter == -1:
            self.pain_frame_counter += 1
            self.last_pain_frame = time_now
        if time_now -self.last_pain_frame > self.pain_frame_time:
            if self.pain_frame_counter == len(self.pain_images) -1:
                self.pain_frame_counter = -1
                self.pain = False
            else:
                self.pain_images.rotate(-1)
                self.pain_frame_counter += 1
                self.last_pain_frame = time_now
        self.image = self.pain_images[0]
        if self.pain == False:
            self.image = random.choice(self.walk_images)

    def attack(self):
        time_now = pg.time.get_ticks()
        if time_now -self.last_attack_time > self.attack_delay:
            self.game.sound_manager.play(4)
            self.game.object_handler.spawn_projectile(self.pos, 'enemy', self.theta +math.pi +random.uniform(-0.3, 0.3), self.attack_damage)
            self.last_attack_time = time_now

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.destination)
        next_x, next_y = next_pos
        self.game.e_lines['start_x'].append(self.x)
        self.game.e_lines['start_y'].append(self.y)
        self.game.e_lines['end_x'].append(self.destination[0] +0.5)
        self.game.e_lines['end_y'].append(self.destination[1] +0.5)
        self.game.e_lines['next_x'].append(next_x)
        self.game.e_lines['next_y'].append(next_y)

        if next_pos not in self.game.object_handler.npc_positions:
            angle = math.atan2(next_y +0.5 -self.y, next_x +0.5 -self.x)
            dx = math.cos(angle) * self.speed * self.game.delta_time
            dy = math.sin(angle) * self.speed * self.game.delta_time
            self.check_wall_collision(dx, dy)
        if self.map_pos == self.destination:
            self.destination = None

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x +dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y +dy * self.size)):
            self.y += dy

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.map_diction
    
    def animate_death(self):
        time_now = pg.time.get_ticks()
        if self.death_frame_counter == -1:
            self.death_frame_counter += 1
            self.last_death_frame = time_now
        if time_now -self.last_death_frame > self.death_frame_time:
            if self.death_frame_counter < 8: 
                self.death_images.rotate(-1)
                self.death_frame_counter += 1
                self.last_death_frame = time_now
        self.image = self.death_images[0]