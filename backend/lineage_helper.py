class DragonNode:
    def __init__(self, dragon_id, generation):
        self.dragon_id = dragon_id
        self.name = ""
        self.gender = "U" #U - Unknown
        self.flight = "Unknown" #Flight of the clan that the dragon belongs to
        self.children = []
        self.descendants_num = 0 #Updates after entire tree has beent built
        self.generation = generation
    def update_metaData(self, name, gender, flight):
        self.name = name
        self.gender = gender
        self.flight = flight
    def add_child(self, child_node):
        self.children.append(child_node)
    def print_metaData(self):
        print(self.id, self.name, self.gender, self.flight)
    
def serialize_tree(node):
    return {
        "id": node.id,
        "name": node.name,
        "gender": node.gender,
        "flight": node.flight,
        "pic": node.portrait_url,
        "children": [serialize_tree(child) for child in node.children]
    }
