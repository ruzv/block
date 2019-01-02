import sprites as s
import blocks as b
import random
import os.path
random.seed(1)
#if not os.path.exists(file_name):

class generate:

    # stuctures
    small_tree = [[6], 
                  [7]]
    medium_tree = [[6], 
                   [7], 
                   [7]]
    big_tree = [[6], 
                [7], 
                [7], 
                [7]]

    def __init__(self, world):
        self.world = world

        # list of what to pick different biomes for world gen
        self.biomes = []

        self.biomes.append(self.gen_forest)
        self.biomes.append(self.gen_feeld)

    # generates a random biome from self.biomes
    def generate(self):
        i = random.randint(0, len(self.biomes)-1)
        return self.biomes[i]()
    
    # forest biome
    def gen_forest(self):
        map = self.fill(32, 90, self.world.blocks.air.id)

        self.fill_random(map, 18, 19, self.world.blocks.grass.id, 95)
        self.fill_random(map, 19, 28, self.world.blocks.dirt.id, 95)
        self.fill_random(map, 28, 89, self.world.blocks.stone.id, 70)
        self.fill_random(map, 28, 35, self.world.blocks.sand.id, 10)

        self.row(map, 0, self.world.blocks.border.id)
        self.row(map, 89, self.world.blocks.border.id)

        for i in range(10):
            self.world.gravity(map)
        for i in range(10):
            self.world.update_grass(map)

        self.add_trees(map, 100)

        return map

    # plane biome (test site)
    def gen_plane(self):
        map = []
        for y in range(90):
            l = []
            for x in range(32):
                l.append(random.randint(0, 3))
            map.append(l)
        map = self.collumn(map, 30, 3)
        map = self.row(map, 0, 4)
        map = self.row(map, 89, 4)
        return map

    # feeld biome
    def gen_feeld(self):
        map = self.fill(32, 90, 0)
        self.fill_random(map, 18, 19, 2, 90)
        self.fill_random(map, 19, 25, 1, 90)
        self.fill_random(map, 25, 90, 3, 70)
        for i in range(10):
            self.world.gravity(map)
        self.row(map, 0, 4)
        self.row(map, 89, 4)
        return map

    # functions for world gen

    # creats a new map with dims x, y filled with block_id
    # used for map initalization(filling with air)
    def fill(self, x, y, block_id):
        map = []
        for yi in range(y):
            l = []
            for xi in range(x):
                l.append(block_id)
            map.append(l)
        return map

    # fills maps row y with block_id
    def row(self, map, y, block_id):
        map[y] = [block_id for i in range(len(map[0]))]

    # fills maps collumn x with block_id
    def collumn(self, map, x, block_id):
        for i in range(len(map)):
            map[i][x] = block_id

    # fills randomly with block_id maps collums form y1 to y2
    def fill_random(self, map, y1, y2, block_id, chance):
        for i in range(y1, y2):
            for k in range(len(map[0])):
                if random.randint(1, 100) <= chance:
                    map[i][k] = block_id

    # adds stuture to map at x, y
    def add_structure(self, map, x, y, structure):
        for yi in range(len(structure)):
            for xi in range(len(structure[0])):
                if structure[yi][xi] != "t":
                    map[y+yi][x+xi] = structure[yi][xi]

    # cheks for treen spawn sites in map and ads trees
    def add_trees(self, map, chance):
        r = 0
        for y in range(5, len(map)):
            for x in range(len(map[0])):
                if map[y][x] == self.world.blocks.grass.id:
                    r += 1
                else:
                    r = 0
                if r == 2:
                    if random.randint(1, 100) <= chance:
                        t = random.randint(1, 3)
                        if t == 1:
                            sturct = self.small_tree
                        elif t == 2:
                            sturct = self.medium_tree
                        elif t == 3:
                            sturct = self.big_tree
                        self.add_structure(map, x+random.randint(0, 1), y-t-1, sturct)
                    r = 0
                

class world:

    # screens coners global pos
    global_screen_pos_x = 0
    global_screen_pos_y = 40
    # the chunk that the player is in
    active_chunk_id = 0

    # screens pos in loaded_map
    screen_map_pos_x = 2560
    screen_map_pos_y = 40

    screen_map_draw_offset_x = 0
    screen_map_draw_offset_y = 0

    # the clock count of world updates
    world_update_count = 1

    loaded_map = [[] for i in range(90)]
    screen_map = []

    def __init__(self, surface):
        self.surface = surface
        self.blocks = b.blocks()
        self.generator = generate(self)

        self.get_loaded_map()
        self.get_screen_map()

    # to file
    def save_chunk(self, chunk, id):
        file = open("saves/"+str(id)+"_chunk-blocks", "w")
        for r in chunk:
            for b in r:
                file.write(str(b)+"\n")
        file.close()
    
    # from file
    def load_chunk(self, id):
        file = open("saves/"+str(id)+"_chunk-blocks", "r")
        chunk = []
        for y in range(90):
            l = []
            for x in range(32):
                a = file.readline()
                l.append(int("".join(list(a)[0:-1])))
            chunk.append(l)
        return chunk
        
    def load_left_chunk(self):
        # unload
        chunk = []
        for i in range(90):
            chunk.append(self.loaded_map[i][128:160])
            del self.loaded_map[i][128:160]
        self.save_chunk(chunk, self.active_chunk_id+2)
        # get new chunk
        if os.path.exists("saves/"+str(self.active_chunk_id-3)+"_chunk-blocks"):
            map = self.load_chunk(self.active_chunk_id-3)
        else:
            map = self.generator.generate()
        # insert new chunk
        for i in range(90):
            self.loaded_map[i] = map[i] + self.loaded_map[i]
        # reset screen pos
        self.active_chunk_id -= 1
        self.screen_map_pos_x += 1280

    def load_right_chunk(self):
        # unload
        chunk = []
        for i in range(90):
            chunk.append(self.loaded_map[i][0:32])
            del self.loaded_map[i][0:32]
        self.save_chunk(chunk, self.active_chunk_id-2)
        # get new chunk
        if os.path.exists("saves/"+str(self.active_chunk_id+3)+"_chunk-blocks"):
            map = self.load_chunk(self.active_chunk_id+3)
        else:
            map = self.generator.generate()
        # insert new chunk
        for i in range(90):
            self.loaded_map[i] += map[i]
        # reset screen pos
        self.active_chunk_id += 1
        self.screen_map_pos_x -= 1290

    # updates screen_maps pos'es
    def move_screen_map(self, dx, dy):
        if self.screen_map_pos_y+dy < 40:
            self.screen_map_pos_y = 40
            self.global_screen_pos_y = 40
        elif self.screen_map_pos_y+dy > 2840:
            self.screen_map_pos_y = 2840
            self.global_screen_pos_y = 2840
        else:
            self.screen_map_pos_y += dy
            self.global_screen_pos_y += dy
        
        self.screen_map_pos_x += dx
        self.global_screen_pos_x += dx

        # check if out of active_chunk
        if self.screen_map_pos_x < 2560:
            self.load_left_chunk()
        elif self.screen_map_pos_x > 3840:
            self.load_right_chunk()

        self.get_screen_map()

    # at world init
    def get_loaded_map(self):
        for i in range(-2, 3):
            if os.path.exists("saves/"+str(self.active_chunk_id+i)+"_chunk-blocks"):
                l = self.load_chunk(self.active_chunk_id+i)
            else:
                l = self.generator.generate()
            for k in range(90):
                self.loaded_map[k] += l[k]

    # gets screen_map_ofsets and pos
    def get_screen_map(self):
        x_pos = int(self.screen_map_pos_x/40)
        y_pos = int(self.screen_map_pos_y/40)

        self.screen_map_draw_offset_x = self.screen_map_pos_x-(x_pos*40)
        self.screen_map_draw_offset_y = self.screen_map_pos_y-(y_pos*40)

        self.screen_map = []
        for y in range(19):
            l = []
            for x in range(33):
                l.append(self.loaded_map[y+y_pos][x+x_pos])
            self.screen_map.append(l)

    def update_grass(self, map):
        spread = []
        for y in range(1, len(map)-1):
            for x in range(0, len(map[0])):
                if map[y][x] == self.blocks.grass.id:
                    # dacay
                    if map[y-1][x] != self.blocks.air.id and map[y-1][x] != self.blocks.tree_stump.id:
                        map[y][x] = self.blocks.dirt.id
                    else: # spread
                        if x != 0:
                            if map[y][x-1] == self.blocks.dirt.id and map[y-1][x-1] == self.blocks.air.id:
                                spread.append([x-1, y])
                        if x != len(map[0])-1:
                            if map[y][x+1] == self.blocks.dirt.id and map[y-1][x+1] == self.blocks.air.id:
                                spread.append([x+1, y])
        for i in spread:
            map[i[1]][i[0]] = self.blocks.grass.id

    # block gravity
    def gravity(self, map):
        for x in range(len(map[0])):
            for y in reversed(range(1, len(map)-1)):
                if self.blocks.get_block_by_id(map[y][x]).has_gravity and  not self.blocks.get_block_by_id(map[y+1][x]).is_solid:
                    map[y+1][x], map[y][x] = map[y][x], map[y+1][x]
    
    # world updates
    def update(self):
        self.world_update_count += 1
        if self.world_update_count%10 == 0:
            self.gravity(self.loaded_map)
            self.get_screen_map()
        if self.world_update_count%120 == 0:
            self.update_grass(self.loaded_map)
            self.get_screen_map()
            # reset count
            self.world_update_count = 1


    def draw(self):
        for y in range(19):
            for x in range(33):
                self.blocks.get_block_by_id(self.screen_map[y][x]).sprite((40*x)-self.screen_map_draw_offset_x, 
                                                                          (40*y)-self.screen_map_draw_offset_y, self.surface)
