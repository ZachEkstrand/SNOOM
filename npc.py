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

        self.attack_dist = random.randint(3, 4)
        self.point_give = 10
        self.speed = 0.076
        self.size = 5
        self.hitbox = 15 / 70
        self.health = 2
        self.attack_damage = 5
        self.last_attack_time = 0
        self.attack_delay = 1000
        self.pain_frame_time = 80
        self.last_pain_frame = pg.time.get_ticks()
        self.pain = False
        self.ray_cast_value = False
        self.pain_frame_counter = -1
        self.destination = None

    def update(self):
        if self.game.scene_manager.current_scene == 'pause_menu': pass 
        else: 
            self.check_animation_time()
            self.run_logic()

        self.get_sprite()

    def run_logic(self):
        self.ray_cast_value = self.ray_cast_player_npc()
        if self.game.scene_manager.round_stopwatch != None:
            if self.game.scene_manager.round_stopwatch.elapsed_time >= 60000:
                self.destination = self.player.map_pos
        if self.pain:
            self.animate_pain()
        elif self.ray_cast_value:
            if self.dist <= self.attack_dist:
                self.attack()
            else:
                self.animate(self.walk_images)
                self.movement()
        elif self.destination:
            self.animate(self.walk_images)
            self.movement()
        else:
            self.image = self.idle_image

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
            self.image = self.pain_images[0]
            self.get_sprite()
            slices = self.slice_image(self.screen_image)
            self.game.object_renderer.dead_npcs_slices.append(slices)
            self.player.kill_streak += 1
            self.game.player.score += self.point_give +self.player.kill_streak * self.player.room_num +self.player.hit_streak * self.player.room_num
            if len([npc for npc in self.game.object_handler.npc_list.keys() if npc.alive]) == 0:
                self.game.object_handler.spawn_key(self.pos)
        else:
            self.game.sound_manager.play(random.randint(8, 10))

    def slice_image(self, full_image):
        slices = []
        num_slices = 30
        for i in range(num_slices):
            slice = []
            slice_image = pg.Surface((full_image.get_width(), full_image.get_height() / num_slices))
            slice_image.fill(0xFFFF00)
            slice_image.set_colorkey(0xFFFF00)
            slice_image.blit(full_image, (0, -(i * (full_image.get_height() / num_slices))))
            x, y = self.screen_pos
            slice.append(slice_image)
            slice.append((x, y +(i * (full_image.get_height() / num_slices))))
            slices.append(slice)
        return slices

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
            self.game.object_handler.spawn_projectile(self.pos, self, self.theta +math.pi +random.uniform(-0.3, 0.3), self.attack_damage, '')
            self.last_attack_time = time_now

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.destination)
        next_x, next_y = next_pos
        
        angle = math.atan2(next_y +0.5 -self.y, next_x +0.5 -self.x)
        speed = self.speed
        dx = math.cos(angle) * speed
        dy = math.sin(angle) * speed
        self.check_collision(dx, dy)
        if self.map_pos == self.destination:
            self.destination = None

    def check_collision(self, dx, dy):
        if self.check_wall(int(self.x +dx * self.size), int(self.y)):
            if self.check_npcs(self.x +dx, self.y):
                self.x += dx
                self.game.object_handler.npc_list[self] = self.pos
        if self.check_wall(int(self.x), int(self.y +dy * self.size)):
            if self.check_npcs(self.x, self.y +dy):
                self.y += dy

        self.game.object_handler.npc_list[self] = self.pos

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.map_diction
    
    def check_npcs(self, x, y):
        for enemy in self.game.object_handler.npc_list.keys():
            if enemy == self:
                continue
            dx = x -enemy.x
            dy = y -enemy.y
            dist = math.hypot(dx, dy)
            if dist <= 0.5:
                return False
        return True

class Boss(NPC):
    def __init__(self, game, path='resources/sprites/npc/elf/walk/7.png', pos=(1, 1),
                 scale=1.2, shift=-0.1, animation_time=100):
        super().__init__(game, path, pos, scale, shift, animation_time)
        self.idle_image = pg.image.load('resources/sprites/npc/elf/walk/7.png').convert_alpha()
        self.death_images = self.get_images('resources/sprites/npc/elf/death')
        self.pain_images = self.get_images('resources/sprites/npc/elf/pain')
        self.walk_images = self.get_images('resources/sprites/npc/elf/walk')

        self.attack_dist = 32
        self.point_give = 30
        self.speed = 0.06
        self.hitbox = 15 / 60
        self.health = 10
        self.max_health = self.health
        self.attack_delay = 1500
        self.powerup = random.choice(['TRIPLE', 'GIANT', '2X DAMAGE', 'BOUNCE', 'LEECH', 'PITCHER', 'STUN', 'COMBO'])
        self.time_of_last_step = 0

    def run_logic(self):
        self.ray_cast_value = self.ray_cast_player_npc()
        if self.game.scene_manager.round_stopwatch != None:
            if self.game.scene_manager.round_stopwatch.elapsed_time >= 60000:
                self.destination = self.player.map_pos
        if self.pain:
            self.animate_pain()
        elif self.ray_cast_value:
            if self.dist <= self.attack_dist:
                self.attack()
            if self.dist > 2:
                self.animate(self.walk_images)
                self.movement()
        elif self.destination:
            self.animate(self.walk_images)
            self.movement()
        else:
            self.image = self.idle_image

    def check_collision(self, dx, dy):
        if self.check_wall(int(self.x +dx * self.size), int(self.y)):
            if self.check_npcs(self.x +dx, self.y):
                self.x += dx
                if self.game.controller_manager:
                    self.time_of_last_step = self.game.controller_manager.footstep(self.time_of_last_step)
                self.game.object_handler.npc_list[self] = self.pos
        if self.check_wall(int(self.x), int(self.y +dy * self.size)):
            if self.check_npcs(self.x, self.y +dy):
                self.y += dy
                if self.game.controller_manager:
                    self.time_of_last_step = self.game.controller_manager.footstep(self.time_of_last_step)
        self.game.object_handler.npc_list[self] = self.pos

    def attack(self):
        time_now = pg.time.get_ticks()
        if time_now -self.last_attack_time > self.attack_delay:
            powerup = self.powerup
            if powerup == 'COMBO':
                powerup = random.choice(['TRIPLE', 'GIANT', '2X DAMAGE', 'BOUNCE', 'LEECH', 'PITCHER', 'STUN'])
            self.game.sound_manager.play(4)
            self.game.object_handler.spawn_projectile(self.pos, self, self.theta +math.pi +random.uniform(-0.3, 0.3), self.attack_damage, powerup)
            if powerup == 'TRIPLE':
                self.game.object_handler.spawn_projectile(self.pos, self, self.theta +math.pi +random.uniform(-0.3, 0.3), self.attack_damage, '')
                self.game.object_handler.spawn_projectile(self.pos, self, self.theta +math.pi +random.uniform(-0.3, 0.3), self.attack_damage, '')
            self.last_attack_time = time_now