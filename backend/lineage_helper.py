class DragonNode:
    def __init__(self, id, name, gender, flight, portrait_url):
        self.id = id
        self.name = name
        self.gender = gender
        self.flight = flight
        self.portrait_url = portrait_url
        self.children = []
        self.descendants_num = 0
    def add_child(self, child_node):
        self.children.append(child_node)
        
def serialize_tree(node):
    return {
        "id": node.id,
        "name": node.name,
        "gender": node.gender,
        "flight": node.flight,
        "pic": node.portrait_url,
        "children": [serialize_tree(child) for child in node.children]
    }
