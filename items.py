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

class items:

    item_ids = [0, 1]
    item_obj = []

    def __init__(self):
        self.dirt =  item(0, "dirt",  "b", block(1), s.dirt_item,  1)
        self.stone = item(1, "stone", "b", block(3), s.stone_item, 20)

        self.item_obj.append(self.dirt)
        self.item_obj.append(self.stone)

    def get_item_by_id(self, id):
        i = self.item_ids.index(id)
        return self.item_obj[i]