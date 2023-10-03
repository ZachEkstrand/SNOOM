import random
from sprite_object import *

path = 'resources/sprites/npc/'
class NPC(AnimatedSprite): #elf cadet
    def __init__(self, game, path=path +'elf/0.png',pos=(1, 1),
                 scale=0.6, shift=0.38, animation_time=100):
        super().__init__(game, path, pos, scale, shift, animation_time)
        path = self.path
        self.attack_images = self.get_images(path +'/attack')
        self.death_images = self.get_images(path +'/death')
        self.pain_images = self.get_images(path +'/pain')
        self.walk_images = self.get_images(path +'/walk')
        self.idle_images = self.get_images(path +'/idle')

        self.point_give = 11
        self.attack_dist = random.randint(3, 6)
        self.attack_delay = 180
        self.speed = 0.025
        self.size = 15
        self.hitbox = self.size / 70
        self.health = 100
        self.attack_damage = 10
        self.attack_frame_counter = 0
        self.attack_frame_num = len(self.attack_images)
        self.alive = True
        self.pain = False
        self.ray_cast_value = False
        self.frame_counter = 0
        self.player_search_trigger = False
        self.key = False

    def update(self):
        if self.game.scene_manager.current_scene == 'pause_menu': pass 
        else: self.check_animation_time()

        self.get_sprite()
        
        if self.game.scene_manager.current_scene == 'pause_menu': pass
        else: self.run_logic()

    def run_logic(self):
        if self.alive:
            self.ray_cast_value = self.ray_cast_player_npc()
            if self.pain:
                self.animate_pain()
            elif self.ray_cast_value:
                self.player_search_trigger = True
                if self.dist < self.attack_dist:
                    self.animate_attack()
                else:
                    self.animate(self.walk_images)
                    self.movement()
            elif self.player_search_trigger:
                self.animate(self.walk_images)
                self.movement()
            else:
                self.animate(self.idle_images)
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
            self.last_seen_player_pos = self.player.map_pos
            return True
        return False
    
    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def take_damage(self, damage):
        self.pain = True
        self.health -= damage
        self.check_health()

    def check_health(self):
        if self.health < 1:
            self.alive = False
            self.game.player.ammo += 2
            self.game.player.score += self.point_give
            if self.key:
                self.game.object_handler.spawn_key(self.pos)

    def animate_pain(self):
        self.animate(self.pain_images)
        if self.animation_trigger:
            self.pain = False

    def animate_attack(self):
        if self.animation_trigger:
            self.attack_images.rotate(-1)
            self.image = self.attack_images[0]
            self.attack_frame_counter += 1
            if self.attack_frame_counter == 1: #frame that the snowball leaves hand
                self.game.object_handler.spawn_projectile(self.pos, 'enemy', self.theta + math.pi +random.uniform(-0.3, 0.3), 10)
            if self.attack_frame_counter == self.attack_frame_num:
                self.attack_frame_counter = 0

    def movement(self):
        next_pos = self.game.pathfinding.get_path(self.map_pos, self.player.map_pos)
        next_x, next_y = next_pos

        if next_pos not in self.game.object_handler.npc_positions:
            angle = math.atan2(next_y +0.5 -self.y, next_x +0.5 -self.x)
            dx = math.cos(angle) * self.speed
            dy = math.sin(angle) * self.speed
            self.check_wall_collision(dx, dy)

    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x +dx * self.size), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y +dy * self.size)):
            self.y += dy

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.map_diction
    
    def animate_death(self):
        if self.frame_counter < len(self.death_images) -1:
            self.death_images.rotate(-1)
            self.image = self.death_images[0]
            self.frame_counter += 1