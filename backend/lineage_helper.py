import math

def calculate_portrait(dragon_id):
    try:
        dragon_id = int(dragon_id)
        portrait_id = math.ceil(dragon_id / 100)
        if dragon_id % 100 == 0:
            portrait_id += 1
        return portrait_id
    except Exception:
        print("Invalid dragon_id: ", dragon_id)
        return 0
    
class DragonNode:
    def __init__(self, dragon_id, generation):
        self.dragon_id = dragon_id
        self.name = ""
        self.gender = "U" #U - Unknown
        self.flight = "" #Flight of the clan that the dragon belongs to
        self.exalted = False
        self.children = []
        self.descendants_num = 0 #Updates after entire tree has beent built
        self.generation = generation
        self.portrait_id = calculate_portrait(int(dragon_id))
        
        
    def update_metaData(self, name, gender, flight, exalted):
        self.name = name
        self.gender = gender
        self.flight = flight
        self.exalted = exalted
    def add_child(self, child_node):
        self.children.append(child_node)
    def print_metaData(self):
        print(self.id, self.name, self.gender, self.flight)

def serialize_tree(node):
    return {
        "dragon_id": node.dragon_id,
        "name": node.name,
        "gender": node.gender,
        "flight": node.flight,
        "generation": node.generation,
        "descendants_num": node.descendants_num,
        "exalted": node.exalted,
        "portrait_id": node.portrait_id,
        "children": [serialize_tree(child) for child in node.children]
    }
