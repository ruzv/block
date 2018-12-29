import sprites as s


class block:
    
    def __init__(self, id, name, sprite, has_gravity, is_solid, break_dorps, hardness):
        self.id = id
        self.name = name
        self.sprite = sprite
        self.has_gravity = has_gravity
        self.is_solid = is_solid
        self.break_dorps = break_dorps
        self.hardness = hardness

class blocks:
    
    block_ids = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    block_obj = []

    def __init__(self):
        self.air =         block(0, "air",         s.air,         False, False, None,   "inf")
        self.dirt =        block(1, "dirt",        s.dirt,        True,  True,  [0, 1], 20)
        self.grass =       block(2, "grass",       s.grass,       True,  True,  [0, 1], 20)
        self.stone =       block(3, "stone",       s.stone,       False, True,  [1, 1], 20)
        self.border =      block(4, "border",      s.air,         False, True,  None,   "inf")
        self.sand =        block(5, "sand",        s.sand,        True,  True,  [2, 1], 20)
        self.tree_leafes = block(6, "tree leafes", s.tree_leafes, True,  True,  None,   20)
        self.tree_stump =  block(7, "tree stump",  s.tree_stump,  True,  True,  None,   20)
        self.water =       block(8, "water",       s.water,       True,  False, None,   20)

        self.block_obj.append(self.air)
        self.block_obj.append(self.dirt)
        self.block_obj.append(self.grass)
        self.block_obj.append(self.stone)
        self.block_obj.append(self.border)
        self.block_obj.append(self.sand)
        self.block_obj.append(self.tree_leafes)
        self.block_obj.append(self.tree_stump)
        self.block_obj.append(self.water)

    def get_block_by_id(self, id):
        i = self.block_ids.index(id)
        return self.block_obj[i]

