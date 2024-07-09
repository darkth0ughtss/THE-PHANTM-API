from flask import Flask, request, jsonify, Response
from models import truths_collection, dares_collection
from bson.objectid import ObjectId

app = Flask(__name__)

# Define the authorization token
AUTH_TOKEN = "Dominos"

def check_auth(request):
    token = request.headers.get('Authorization')
    if token == AUTH_TOKEN:
        return True
    else:
        return False

@app.route('/add', methods=['POST'])
def add_truth_or_dare():
    if not check_auth(request):
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    category = data.get('category')
    content = data.get('content')
    
    if category not in ['truth', 'dare']:
        return jsonify({'error': 'Invalid category'}), 400
    
    collection = truths_collection if category == 'truth' else dares_collection
    result = collection.insert_one({'content': content})
    return jsonify({'message': 'Added successfully', 'id': str(result.inserted_id)}), 201

@app.route('/add_bulk', methods=['POST'])
def add_bulk_truth_or_dare():
    if not check_auth(request):
        return jsonify({'error': 'Unauthorized'}), 403

    data = request.json
    category = data.get('category')
    contents = data.get('contents')
    
    if category not in ['truth', 'dare']:
        return jsonify({'error': 'Invalid category'}), 400
    
    if not isinstance(contents, list):
        return jsonify({'error': 'Contents should be a list of questions'}), 400
    
    collection = truths_collection if category == 'truth' else dares_collection
    documents = [{'content': content} for content in contents]
    result = collection.insert_many(documents)
    return jsonify({'message': 'Added successfully', 'ids': [str(id) for id in result.inserted_ids]}), 201

@app.route('/get/<category>', methods=['GET'])
def get_truth_or_dare(category):
    if category not in ['truth', 'dare']:
        return jsonify({'error': 'Invalid category'}), 400
    
    collection = truths_collection if category == 'truth' else dares_collection
    pipeline = [{'$sample': {'size': 1}}]  # Randomly sample one document
    item = list(collection.aggregate(pipeline))
    
    if item:
        return Response(item[0]['content'], mimetype='text/plain'), 200
    else:
        return Response('No item found', mimetype='text/plain'), 404

@app.route('/get/<category>/<id>', methods=['GET'])
def get_truth_or_dare_by_id(category, id):
    if category not in ['truth', 'dare']:
        return jsonify({'error': 'Invalid category'}), 400
    
    collection = truths_collection if category == 'truth' else dares_collection
    item = collection.find_one({'_id': ObjectId(id)}, {'content': 1, '_id': 0})
    
    if item:
        return Response(item['content'], mimetype='text/plain'), 200
    else:
        return Response('Not found', mimetype='text/plain'), 404

if __name__ == '__main__':
    app.run(debug=True)
