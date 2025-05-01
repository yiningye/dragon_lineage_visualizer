from flask import Flask, request, jsonify

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
def get_lineage():
    dragon_id = request.args.get('dragonId')
    max_gen = int(request.args.get('maxGen', 3))  # default to 3 if missing

    data = dummy_lineage_data.get(dragon_id)

    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Dragon not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
