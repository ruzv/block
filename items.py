import sprites as s

class item:

    def __init__(self, id, name, type, type_spesifics, sprite, max_stack):
        self.id = id
        self.name = name
        self.type = type
        self.type_spesifics = type_spesifics
        self. sprite = sprite
        self.max_stack = max_stack

class block:
    def __init__(self, block_id):
        self.block_id = block_id

class pickaxe:
    def __init__(self, strength, sprite):
        self.strength = strength
        self.sprite = sprite

class items:

    item_ids = [0, 1, 2, 3]
    item_obj = []

    def __init__(self):
        self.dirt =         item(0, "dirt",  "b", block(1), s.dirt_item,  20)
        self.stone =        item(1, "stone", "b", block(3), s.stone_item, 20)
        self.sand =         item(2, "sand",  "b", block(5), s.sand_item,  20)
        self.wood_pickaxe = item(3, "wood pickaxe", "p", pickaxe(1, None), s.wood_pickaxe_item, 1)

        self.item_obj.append(self.dirt)
        self.item_obj.append(self.stone)
        self.item_obj.append(self.sand)
        self.item_obj.append(self.wood_pickaxe)

    def get_item_by_id(self, id):
        i = self.item_ids.index(id)
        return self.item_obj[i]