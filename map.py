import random

class Map:
    def __init__(self, game):
        self.game = game
        self.map_grid = []
        self.map_diction = {}
        self.space_indexes = []
        self.rows = 32
        self.cols = 32
        self.generate_map()
        self.get_map()

    def generate_map(self):
        self.create_blank_map()
        self.cut_out_shapes()
        self.create_player_spawnpoint()
        self.print_map()

    def create_blank_map(self):
        wall_weight = 30
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(random.choices([1, 2, 3, 4, 5, 6, 7, 8], [wall_weight, wall_weight, wall_weight, wall_weight, 1, 1, 1, 1])[0])
            self.map_grid.append(row)

    def cut_out_shapes(self):
        shapeNum = 40
        self.cut_shape(x=random.randint(1, 30), y=random.randint(1, 30))
        for i in range(shapeNum -1):
            index = random.choice(self.space_indexes)
            x = index[0]
            y = index[1]
            self.cut_shape(x,y)

    def cut_shape(self, x, y):
        destroy = self.destroy
        shape = random.choice(('U', 'L', 'rect', 'line'))

        if shape == 'U':
            width = random.randint(3,15)
            arm1_height = random.randint(2, 20)
            arm2_height = random.randint(2, 20)
            angle = random.choice(('up', 'right', 'down', 'left'))

            for i in range(width):
                if angle == 'up':
                    destroy(x +i, y)
                if angle == 'right':
                    destroy(x, y +i)
                if angle == 'down':
                    destroy(x -i, y)
                if angle == 'left':
                    destroy(x, y -i)

            for i in range(arm1_height):
                if angle == 'up':
                    destroy(x, y -i)
                if angle == 'right':
                    destroy(x +i, y)
                if angle == 'down':
                    destroy(x, y +i)
                if angle == 'left':
                    destroy(x -i, y)

            for i in range(arm2_height):
                if angle == 'up':
                    destroy(x +width -1, y -i)
                if angle == 'right':
                    destroy(x +i, y +width -1)
                if angle == 'down':
                    destroy(x -width +1, y +i)
                if angle == 'left':
                    destroy(x -i, y -width +1)

        if shape == 'L':
            width = random.randint(2, 15)
            height = random.randint(2, 30)
            angle = random.choice(('up', 'right', 'down', 'left'))

            for i in range(width):
                if angle == 'up':
                    destroy(x +i, y)
                if angle == 'right':
                    destroy(x, y +i)
                if angle == 'down':
                    destroy(x -i, y)
                if angle == 'left':
                    destroy(x, y -i)

            for i in range(height):
                if angle == 'up':
                    destroy(x +width -1, y -i)
                if angle == 'right':
                    destroy(x +i, y +width -1)
                if angle == 'down':
                    destroy(x -width +1, y +i)
                if angle == 'left':
                    destroy(x -i, y -width +1)

        if shape == 'rect':
            width = random.randint(2, 10)
            height = random.randint(2, 10)
            angle = random.choice(('top-right', 'bottom-right', 'bottom-left', 'top-left'))

            for i in range(height):
                for j in range(width):
                    if angle == 'top-right':
                        destroy(x +j, y -i)
                    if angle == 'bottom-right':
                        destroy(x +j, y +i)
                    if angle == 'bottom-left':
                        destroy(x -j, y +i)
                    if angle == 'top-left':
                        destroy(x -j, y -i)

        if shape == 'line':
            width = 1
            height = random.randint(2, 7)
            angle = random.choice(('up', 'right', 'down', 'left'))

            for i in range(height):
                if angle == 'up':
                    destroy(x, y -i)
                if angle == 'right':
                    destroy(x +i, y)
                if angle == 'down':
                    destroy(x, y +i)
                if angle == 'left':
                    destroy(x -i, y)

    def destroy(self, x, y):
        if self.is_not_border(x, y):
            try:
                self.map_grid[y][x] = False
                if (x, y) not in self.space_indexes:
                    self.space_indexes.append((x, y))
            except:
                print('Destroy Error:', (x, y))

    def is_not_border(self, x, y):
        if x <= 0 or x >= self.rows -1 or y <= 0 or y >= self.cols -1:
            return False
        return True

    def create_player_spawnpoint(self):
        self.space_indexes.sort()
        self.player_spawn_x = self.space_indexes[0][0]
        self.player_spawn_y = self.space_indexes[0][1]
        self.player_pos = self.player_spawn_x +0.5, self.player_spawn_y +0.5

        if (self.player_spawn_x +1, self.player_spawn_y) in self.space_indexes:
            self.map_grid[self.player_spawn_y][self.player_spawn_x -1] = 9
            self.player_angle = 0
        else:
            self.map_grid[self.player_spawn_y -1][self.player_spawn_x] = 9
            self.player_angle = 1.5

    def get_map(self):
        for j, row in enumerate(self.map_grid):
            for i, value in enumerate(row):
                if value:
                    self.map_diction[(i, j)] = value
                    
    def print_map(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.map_grid[i][j] == False:
                    if i == self.player_spawn_y and j == self.player_spawn_x:
                        print('P', end=' ')
                    else:
                        print(' ', end=' ')
                else:
                    print(self.map_grid[i][j], end=' ')
            print()