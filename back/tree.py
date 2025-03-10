import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tree = {
    'id': str(uuid.uuid4()),
    'name': 'Иван Иванович',
    'photo': 'https://example.com/photo.jpg',
    'birthDate': '1950-01-01',
    'deathDate': '2020-01-01',
    'children': [
        {
            'id': str(uuid.uuid4()),
            'name': 'Алексей Иванович',
            'photo': 'https://example.com/photo1.jpg',
            'birthDate': '1980-01-01',
            'deathDate': '2015-01-01',
            'children': [],
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Мария Ивановна',
            'photo': 'https://example.com/photo2.jpg',
            'birthDate': '1985-01-01',
            'deathDate': '2018-01-01',
            'children': [
                {
                    'id': str(uuid.uuid4()),
                    'name': 'Дмитрий Алексеевич',
                    'photo': 'https://example.com/photo3.jpg',
                    'birthDate': '2010-01-01',
                    'deathDate': '',
                    'children': [],
                }
            ],
        },
    ],
}


@app.route('/api/tree', methods=['GET'])
def get_tree():
    return jsonify(tree)


@app.route('/api/tree/update', methods=['POST'])
def update_node():
    json = request.json
    if json is None:
        return jsonify({'status': 'error', 'message': 'Узел не найден'}), 404
    node_data = json.get('nodeData')
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
        return jsonify(
            {'status': 'success', 'message': 'Узел успешно обновлен'}
        )
    else:
        return jsonify({'status': 'error', 'message': 'Узел не найден'}), 404


@app.route('/api/tree/add', methods=['POST'])
def add_node():
    json = request.json
    if json is None:
        return jsonify({'status': 'error', 'message': 'Узел не найден'}), 404
    node_data = json.get('nodeData')
    new_node = {
        'id': str(uuid.uuid4()),
        'name': node_data['name'],
        'photo': node_data.get('photo', ''),
        'birthDate': node_data.get('birthDate', ''),
        'deathDate': node_data.get('deathDate', ''),
        'children': [],
    }
    tree['children'].append(new_node)
    return jsonify({'message': 'Новый узел добавлен'})


@app.route('/api/tree/delete', methods=['DELETE'])
def delete_node():
    json = request.json
    if json is None:
        return jsonify({'status': 'error', 'message': 'Узел не найден'}), 404
    node_id = json.get('id')

    def delete_node_recursively(node, parent=None):
        if node['id'] == node_id:
            if parent:
                parent['children'] = [
                    child
                    for child in parent['children']
                    if child['id'] != node_id
                ]
            return True
        for child in node.get('children', []):
            if delete_node_recursively(child, node):
                return True
        return False

    if delete_node_recursively(tree):
        return jsonify({'status': 'success', 'message': 'Узел успешно удален'})
    else:
        return jsonify({'status': 'error', 'message': 'Узел не найден'}), 404


if __name__ == '__main__':
    app.run(host='localhost', debug=True)
