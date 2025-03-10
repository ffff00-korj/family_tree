from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех доменов

# Пример дерева с уникальными ID
tree = {
    "id": str(uuid.uuid4()),  # Генерация уникального ID для корня
    "name": "Иван Иванович",
    "photo": "https://example.com/photo.jpg",
    "birthDate": "1950-01-01",
    "deathDate": "2020-01-01",
    "children": [
        {
            "id": str(uuid.uuid4()),
            "name": "Алексей Иванович",
            "photo": "https://example.com/photo1.jpg",
            "birthDate": "1980-01-01",
            "deathDate": "2015-01-01",
            "children": []
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Мария Ивановна",
            "photo": "https://example.com/photo2.jpg",
            "birthDate": "1985-01-01",
            "deathDate": "2018-01-01",
            "children": [
                {
                    "id": str(uuid.uuid4()),
                    "name": "Дмитрий Алексеевич",
                    "photo": "https://example.com/photo3.jpg",
                    "birthDate": "2010-01-01",
                    "deathDate": "",
                    "children": []
                }
            ]
        }
    ]
}


# Маршрут для получения дерева
@app.route('/api/tree', methods=['GET'])
def get_tree():
    return jsonify(tree)


# Маршрут для обновления узла
@app.route('/api/tree/update', methods=['POST'])
def update_node():
    node_data = request.json.get('nodeData')
    node_id = node_data['id']
    
    def update_node_recursively(node):
        if node['id'] == node_id:
            node.update(node_data)
            return True
        for child in node.get('children', []):
            if update_node_recursively(child):
                return True
        return False

    if update_node_recursively(tree):
        return jsonify({"status": "success", "message": "Узел успешно обновлен"})
    else:
        return jsonify({"status": "error", "message": "Узел не найден"}), 404

# Маршрут для добавления нового узла
@app.route('/api/tree/add', methods=['POST'])
def add_node():
    node_data = request.json['nodeData']
    new_node = {
        "id": str(uuid.uuid4()),
        "name": node_data['name'],
        "photo": node_data.get('photo', ''),
        "birthDate": node_data.get('birthDate', ''),
        "deathDate": node_data.get('deathDate', ''),
        "children": []
    }
    tree_data['children'].append(new_node)
    return jsonify({"message": "Новый узел добавлен"})

# Маршрут для удаления узла
@app.route('/api/tree/delete', methods=['DELETE'])
def delete_node():
    node_id = request.json.get('id')

    def delete_node_recursively(node, parent=None):
        if node['id'] == node_id:
            if parent:
                parent['children'] = [child for child in parent['children'] if child['id'] != node_id]
            return True
        for child in node.get('children', []):
            if delete_node_recursively(child, node):
                return True
        return False

    if delete_node_recursively(tree):
        return jsonify({"status": "success", "message": "Узел успешно удален"})
    else:
        return jsonify({"status": "error", "message": "Узел не найден"}), 404


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

