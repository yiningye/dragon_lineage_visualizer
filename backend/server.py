from flask import Flask, request, jsonify, render_template
from backend.dragon_tree import build_lineage_tree  # your logic to construct trees
import os
import json

app = Flask(__name__)

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

@app.route('/api/lineage')
@app.route('/')
@app.route('/index')
@app.route('/')
def index():
    return render_template("frontend/index.html", dragon_id="1234")

def get_lineage():
    dragon_id = request.args.get('dragonId')
    max_gen = int(request.args.get('maxGen', 3))
    filepath = f'data/{dragon_id}.json'

    # For testing: load from dummy data
    filepath = f'lineage_data/{dragon_id}.json'
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
        return jsonify(data)

    # Otherwise generate from live scraping/tree logic
    try:
        root_node = build_lineage_tree(dragon_id, max_gen)
        from dragon_tree import serialize_tree
        tree_json = serialize_tree(root_node)

        # Optional: save to file
        os.makedirs("lineage_data", exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(tree_json, f, indent=2)

        return jsonify(tree_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port = "8000")
