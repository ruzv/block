import pygame
import sprites as s
import world as w
import player as p


pygame.init()
display = pygame.display.set_mode([1280, 720])
pygame.display.set_caption("7_day_chalange")
clock = pygame.time.Clock()

world = w.world(display)
player = p.player(display, world)

que = []    
max_que_len = 4
def event_handler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN and len(que) < max_que_len:
            if event.key == pygame.K_a and "a" not in que:
                que.append("a")
            if event.key == pygame.K_d and "d" not in que:
                que.append("d")
            if event.key == pygame.K_w and "w" not in que:
                que.append("w")
            if event.key == pygame.K_s and "s" not in que:
                que.append("s")
            if event.key == pygame.K_e:
                player.inventory.is_inventory_open = not player.inventory.is_inventory_open
            if event.key == pygame.K_1:
                player.inventory.hotbar_currsor = 0
            if event.key == pygame.K_2:
                player.inventory.hotbar_currsor = 1
            if event.key == pygame.K_3:
                player.inventory.hotbar_currsor = 2
            if event.key == pygame.K_4:
                player.inventory.hotbar_currsor = 3
            if event.key == pygame.K_5:
                player.inventory.hotbar_currsor = 4
            if event.key == pygame.K_SPACE and "space" not in que:
                que.append("space")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a and "a" in que:
                que.remove("a")
            if event.key == pygame.K_d and "d" in que:
                que.remove("d")
            if event.key == pygame.K_w and "w" in que:
                que.remove("w")
            if event.key == pygame.K_s and "s" in que:
                que.remove("s")
            if event.key == pygame.K_SPACE and "space" in que:
                que.remove("space")

        if event.type == pygame.MOUSEBUTTONDOWN and len(que) < max_que_len:
            p = pygame.mouse.get_pressed()
            if p[0] == 1 and "l_mouse" not in que:
                que.append("l_mouse")
            if p[2] == 1:
                player.inventory.pick_up_item()
                player.place_block()

        if event.type == pygame.MOUSEBUTTONUP:
            p = pygame.mouse.get_pressed()
            if p[0] != 1 and "l_mouse" in que:
                que.remove("l_mouse")

    if "a" in que:
        player.is_moving_left = True
    else:
        player.is_moving_left = False

    if "d" in que:
        player.is_moving_right = True
    else:
        player.is_moving_right = False

    if "space" in que:
        player.start_jumping()

    else:
        player.is_jumping = False

    if "s" in que:
        pass

    if "l_mouse" in que:
        player.start_block_breaking()
    else:
        player.stop_block_breaking()

    print(que)

def update():
    event_handler()
    world.update()
    player.update()

def draw():
    display.fill([255, 255, 255])

    world.draw()
    player.draw()
    player.draw_cursor()
    player.inventory.draw()
    player.draw_block_breaking_progress_bar()

    pygame.display.update()

while True:

    update()
    draw()

    clock.tick(20)
    