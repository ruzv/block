import sprites as s


class block:
    
    def __init__(self, id, name, sprite, has_gravity, is_solid, break_dorps):
        self.id = id
        self.name = name
        self.sprite = sprite
        self.has_gravity = has_gravity
        self.is_solid = is_solid
        self.break_dorps = break_dorps

class blocks:
    
    block_ids = [0, 1, 2, 3, 4]
    block_obj = []

    def __init__(self):
        self.air =    block(0, "air",    s.air,   False, False, None)
        self.dirt =   block(1, "dirt",   s.dirt,  True,  True,  [0, 1])
        self.grass =  block(2, "grass",  s.grass, True,  True,  [0, 1])
        self.stone =  block(3, "stone",  s.stone, False, True,  [1, 1])
        self.border = block(4, "border", s.air,   False, True,  None)

        self.block_obj.append(self.air)
        self.block_obj.append(self.dirt)
        self.block_obj.append(self.grass)
        self.block_obj.append(self.stone)
        self.block_obj.append(self.border)

    def get_block_by_id(self, id):
        i = self.block_ids.index(id)
        return self.block_obj[i]

