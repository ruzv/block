import pygame


pygame.font.init()
font = pygame.font.SysFont("comicsansms", 20)

def player(x, y, surface):
    pygame.draw.rect(surface, (102, 255, 102), [x, y, 40, 80])

# blocks

def air(x, y, surface):
    pass

def dirt(x, y, surface):
    pygame.draw.rect(surface, (77, 40, 0), [x, y, 40, 40])

def grass(x, y, surface):
    pygame.draw.rect(surface, (77, 40, 0), [x, y, 40, 40])
    pygame.draw.rect(surface, (51, 102, 0), [x, y, 40, 8])

def stone(x, y, surface):
    pygame.draw.rect(surface, (64, 64, 64), [x, y, 40, 40])


# items

def inventory(x, y, surface):
    pygame.draw.rect(surface, (153, 153, 102), [x, y, 206, 165]) 
    for i in range(6):
        pygame.draw.line(surface, (0, 0, 0), [x+(i*41), y], [x+(i*41), y+164], 2)
    for i in range(5):
        pygame.draw.line(surface, (0, 0, 0), [x, y+(i*41)], [x+205, y+(i*41)], 2)

def inventory_currsor_empty(x, y, surface):
    pygame.draw.rect(surface, (204, 255, 51), [x, y, 42, 42], 4)

def inventory_currsor_full(x, y, surface):
    pygame.draw.rect(surface, (255, 153, 102), [x, y, 42, 42], 4)

def hotbar(x, y, surface):
    pygame.draw.rect(surface, (153, 153, 102), [x, y, 206, 42]) 
    for i in range(6):
        pygame.draw.line(surface, (0, 0, 0), [x+(i*41), y], [x+(i*41), y+41], 2)
    for i in range(2):
        pygame.draw.line(surface, (0, 0, 0), [x, y+(i*41)], [x+205, y+(i*41)], 2)

def hotbar_currsor(x, y, surface):
    pygame.draw.rect(surface, (204, 153, 0), [x, y, 42, 42], 4)


def dirt_item(x, y, surface, amount):
    t = font.render(str(amount), True, (0, 0, 0))
    pygame.draw.rect(surface, (77, 40, 0), [x, y, 30, 30])
    surface.blit(t, [x+20, y+20])

def stone_item(x, y, surface, amount):
    t = font.render(str(amount), True, (0, 0, 0))
    pygame.draw.rect(surface, (64, 64, 64), [x, y, 30, 30])
    surface.blit(t, [x+20, y+20])