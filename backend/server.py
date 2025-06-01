from flask import Flask, request, jsonify, render_template
from scraping import fetch_dragon_lineage  # your logic to construct trees
from lineage_helper import serialize_tree

import os
import json


template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend"))
app = Flask(__name__, template_folder=template_dir)

dummy_lineage_data = {
    "1234": {
        "name": "Dragon 1234",
        "children": [
            {"name": "Child 1", "children": []},
            {"name": "Child 2", "children": [
                {"name": "Grandchild 1", "children": []}
            ]}
        ]
    }
}

@app.route('/index')
@app.route('/')


def index():
    return render_template("index.html", dragon_id="")

@app.route('/api/lineage')
def get_lineage():
    
    dragon_id = request.args.get('dragonId')
    max_gen = int(request.args.get('maxGen', 3))
    exalted = request.args.get('excludeExalted')
    print("Get lienage of:", dragon_id, max_gen, exalted)
    # For testing: load from dummy data
    filepath = f'data/dragon_tree.json'
    # if os.path.exists(filepath):
    #     with open(filepath, 'r') as f:
    #         data = json.load(f)
    #     return jsonify(data)

    # Otherwise generate from live scraping/tree logic
    try:
        root_node = fetch_dragon_lineage(dragon_id, max_gen, exalted)
        tree_json = serialize_tree(root_node)

        # Optional: save to file
        with open(filepath, 'w') as f:
            json.dump(tree_json, f, indent=2)

        return jsonify(tree_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = "8000")
