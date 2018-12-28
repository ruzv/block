import sprites as s
import items as i
import pygame
import math


class inventory:

    inventory_size = 25

    inventory_item_ids = ["e" for i in range(inventory_size)]
    inventory_item_amounts = [0 for i in range(inventory_size)]

    is_inventory_open = False
    is_inventory_currsor = False

    inventory_currsor_x = 0
    inventory_currsor_y = 0

    pick_up_item_id = "e"
    pick_up_item_amount = 0

    inventory_currsor = 0
    hotbar_currsor = 0


    def __init__(self, surface, items):
        self.surface = surface
        self.items = items

    def add_item(self, item_id, amount):
        for i in range(0, self.inventory_size):
            if self.inventory_item_ids[i] == item_id:
                if self.inventory_item_amounts[i] < self.items.get_item_by_id(item_id).max_stack:
                    self.inventory_item_amounts[i] += 1
                    return None
        for i in range(0, self.inventory_size):
            if self.inventory_item_ids[i] == "e":
                self.inventory_item_ids[i] = item_id
                self.inventory_item_amounts[i] = 1
                return None


    def pick_up_item(self):
        if self.is_inventory_open:
            if self.inventory_currsor_x >= 0 and self.inventory_currsor_x <= 4 and self.inventory_currsor_y >= 0 and self.inventory_currsor_y <= 3:
                print("hello")
                i = (self.inventory_currsor_y*5) + self.inventory_currsor_x+5
                self.inventory_item_ids[i], self.pick_up_item_id = self.pick_up_item_id, self.inventory_item_ids[i]
                self.inventory_item_amounts[i], self.pick_up_item_amount = self.pick_up_item_amount, self.inventory_item_amounts[i]

    def update(self):
        print("hell0")
        print("dosi")

    def draw_inventory(self, x, y):
        s.inventory(x, y, self.surface)
        i = 5
        mx, my = pygame.mouse.get_pos()
        mx -= 1053
        my -= 20
        self.inventory_currsor_x = int(mx/41)
        self.inventory_currsor_y = int(my/41)
        for yi in range(4):
            for xi in range(5):
                if xi == self.inventory_currsor_x and yi == self.inventory_currsor_y:
                    self.draw_inventory_currsor(x+(41*xi), y+(41*yi))
                elif self.inventory_item_ids[i] != "e":
                    self.items.get_item_by_id(self.inventory_item_ids[i]).sprite(x+6+(xi*41), y+6+(yi*41), self.surface, self.inventory_item_amounts[i])
                i += 1

    def draw_inventory_currsor(self, x, y):
        if self.pick_up_item_id == "e":
            s.inventory_currsor_empty(x, y, self.surface)
            i = (self.inventory_currsor_y*5) + self.inventory_currsor_x+5
            if self.inventory_item_ids[i] != "e":
                self.items.get_item_by_id(self.inventory_item_ids[i]).sprite(x+6, y+6, self.surface, self.inventory_item_amounts[i])
        else:
            s.inventory_currsor_full(x, y, self.surface)
            self.items.get_item_by_id(self.pick_up_item_id).sprite(x+6, y+6, self.surface, self.pick_up_item_amount)

    def draw_hotbar(self, x, y):
        s.hotbar(x, y, self.surface)
        for i in range(5):
            if i == self.hotbar_currsor:
                s.hotbar_currsor(x+(41*i), y, self.surface)
            if self.inventory_item_ids[i] != "e":
                self.items.get_item_by_id(self.inventory_item_ids[i]).sprite(x+6+(i*41), y+6, self.surface, self.inventory_item_amounts[i])
    
    def draw(self):
        if self.is_inventory_open:
            self.draw_inventory(1054, 20)
            self.draw_hotbar(1054, 205)
        else:
            self.draw_hotbar(1054, 20)

class player:

    screen_pos_x = 0
    screen_pos_y = 0

    global_pos_x = 620
    global_pos_y = 40

    currsor_pos_x = 0
    currsor_pos_y = 0
    currsor_lenght = 80

    bottom_collision_points = [[0, 79], [39, 79]]

    right_collision_points = [[39, 0], [39, 40], [39, 79]]
    left_collision_points = [[0, 0], [0, 40], [0, 79]]

    top_collision_points = [[0, 0], [39, 0]]

    is_moving_right = False
    is_moving_left = False
    horizontal_movement_speed = 10

    is_gravity = False
    gravity_speed = 10
    gs = 10

    is_jumping = False
    jump_height = 20

    def __init__(self, surface, world):
        self.surface = surface
        self.world = world
        self.items = i.items()
        self.inventory = inventory(surface, self.items)
        self.get_screen_pos()
        self.get_cursor_pos()

    def get_screen_pos(self):
        self.screen_pos_x = self.global_pos_x-self.world.global_screen_pos_x
        self.screen_pos_y = self.global_pos_y-self.world.global_screen_pos_y

    def get_angle(self, x1, y1, x2, y2):
        x = x2 - x1
        y = -(y2 - y1)
        a = math.atan2(y, x)
        return -a

    def get_distance(self, x1, y1, x2, y2):
        x = x2 - x1
        y = y2 - y1
        d = math.sqrt((x**2)+(y**2))
        return d

    def get_cursor_pos(self):
        mpx, mpy = pygame.mouse.get_pos()
        a = self.get_angle(self.screen_pos_x+20, self.screen_pos_y+20, mpx, mpy)
        d = self.get_distance(self.screen_pos_x+20, self.screen_pos_y+20, mpx, mpy)
        if d >= 80:
            self.currsor_pos_x = (math.cos(a)*self.currsor_lenght)+self.screen_pos_x+20
            self.currsor_pos_y = (math.sin(a)*self.currsor_lenght)+self.screen_pos_y+20
        else:
            self.currsor_pos_x = (math.cos(a)*d)+self.screen_pos_x+20
            self.currsor_pos_y = (math.sin(a)*d)+self.screen_pos_y+20

    def break_block(self):
        x = int((self.world.screen_map_pos_x+self.currsor_pos_x)/40)
        y = int((self.world.screen_map_pos_y+self.currsor_pos_y)/40)
        d = self.world.blocks.get_block_by_id(self.world.loaded_map[y][x]).break_dorps
        if d != None:
            self.inventory.add_item(d[0], d[1])
        self.world.loaded_map[y][x] = 0
        self.world.get_screen_map()

    def is_block_colliding(self, x, y, collision_points):
        collision = False
        for p in collision_points:
            i = self.world.screen_map[int((p[1]+y+self.world.screen_map_draw_offset_y)/40)][int((p[0]+x+self.world.screen_map_draw_offset_x)/40)]
            if self.world.blocks.get_block_by_id(i).is_solid:
                collision = True
                break
        return collision

    def move_horizontaly(self):
        if self.is_moving_right:
            if not self.is_block_colliding(self.screen_pos_x+self.horizontal_movement_speed, self.screen_pos_y, self.right_collision_points):
                self.global_pos_x += self.horizontal_movement_speed
                self.world.move_screen_map(self.horizontal_movement_speed, 0)
                self.get_screen_pos()
            else:
                hms = self.horizontal_movement_speed
                while self.is_block_colliding(self.screen_pos_x+hms, self.screen_pos_y, self.right_collision_points):
                    hms -= 1
                    if hms <= 0:
                        hms = 0
                        break
                self.global_pos_x += hms
                self.world.move_screen_map(hms, 0)
                self.is_moving_right = False
                self.get_screen_pos()
            
        if self.is_moving_left:
            if not self.is_block_colliding(self.screen_pos_x-self.horizontal_movement_speed, self.screen_pos_y, self.left_collision_points):
                self.global_pos_x -= self.horizontal_movement_speed
                self.world.move_screen_map(-self.horizontal_movement_speed, 0)
                self.get_screen_pos()
            else:
                hms = self.horizontal_movement_speed
                while self.is_block_colliding(self.screen_pos_x-hms, self.screen_pos_y, self.left_collision_points):
                    hms -= 1
                    if hms <= 0:
                        hms = 0
                        break
                self.global_pos_x -= hms
                self.world.move_screen_map(-hms, 0)
                self.is_moving_left = False
                self.get_screen_pos()

    def is_falling(self):
        if not self.is_block_colliding(self.screen_pos_x, self.screen_pos_y+1, self.bottom_collision_points):
            if not self.is_gravity and not self.is_jumping:
                self.is_gravity = True
                self.gs = self.gravity_speed
            
    def gravity(self):
        if self.is_gravity:
            if not self.is_block_colliding(self.screen_pos_x, self.screen_pos_y+self.gs, self.bottom_collision_points):
                self.global_pos_y += self.gs
                if self.screen_pos_y >= 340:
                    self.world.move_screen_map(0, self.gs)
                self.get_screen_pos()
                self.gs += 1
            else:
                while self.is_block_colliding(self.screen_pos_x, self.screen_pos_y+self.gs, self.bottom_collision_points):
                    self.gs -= 1
                    if self.gs <= 0:
                        self.gs = 0
                        break
                self.global_pos_y += self.gs
                if self.screen_pos_y >= 340:
                    self.world.move_screen_map(0, self.gs)                
                self.get_screen_pos()
                self.is_gravity = False

    def start_jumping(self):
        if self.is_block_colliding(self.screen_pos_x, self.screen_pos_y+1, self.bottom_collision_points):
            self.jh = self.jump_height
            self.is_jumping = True

    def jumping(self):
        if self.is_jumping:
            if not self.is_block_colliding(self.screen_pos_x, self.screen_pos_y-self.jh, self.top_collision_points):
                self.global_pos_y -= self.jh
                if self.screen_pos_y <= 340:
                    self.world.move_screen_map(0, -self.jh)
                self.get_screen_pos()
                self.jh -= 1
                if self.jh <= 0:
                    self.is_jumping = False
            else:
                while self.is_block_colliding(self.screen_pos_x, self.screen_pos_y-self.jh, self.top_collision_points):
                    self.jh -= 1
                    if self.jh <= 0:
                        self.jh = 0
                        break
                self.global_pos_y -= self.jh
                if self.screen_pos_y <= 340:
                    self.world.move_screen_map(0, self.jh) 
                self.get_screen_pos()
                self.is_jumping = False



    def update(self):
        self.is_falling()
        self.gravity()
        self.jumping()
        self.move_horizontaly()

        self.get_cursor_pos()

        # for i, a in zip(self.inventory.inventory_item_ids, self.inventory.inventory_item_amounts):
        #     print(i, a, end=' ')
        # print()


    def draw_cursor(self):
        pygame.draw.line(self.surface, (0, 0, 0), [self.screen_pos_x+20, self.screen_pos_y+20], [self.currsor_pos_x, self.currsor_pos_y], 4)

    def draw(self):
        s.player(self.screen_pos_x, self.screen_pos_y, self.surface)