from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from pymongo import MongoClient
from bson import ObjectId, json_util
import json

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017/')
db = client['blogdatabase']
posts_collection = db['posts']

# Health check route
@app.route('/check')
def home():
    return jsonify(message="Hello, World! This is the backend.")

class PostList(Resource):
    def get(self):
        posts = list(posts_collection.find())
        return json.loads(json_util.dumps(posts)), 200

    def post(self):
        data = request.get_json()
        new_post = {
            'title': data['title'],
            'content': data['content'],
            'scale': data.get('scale', 'default_scale_value')  # Use 'scale' if provided, else default value
        }
        result = posts_collection.insert_one(new_post)
        return json.loads(json_util.dumps(new_post)), 201

class Post(Resource):
    def get(self, post_id):
        post = posts_collection.find_one({'_id': ObjectId(post_id)})
        if post:
            return json.loads(json_util.dumps(post)), 200
        return {'error': 'Post not found'}, 404

    def put(self, post_id):
        data = request.get_json()
        updated_post = {
            'title': data['title'],
            'content': data['content'],
            'scale': data.get('scale', 'default_scale_value')  # Use 'scale' if provided, else default value
        }
        result = posts_collection.update_one({'_id': ObjectId(post_id)}, {'$set': updated_post})
        if result.matched_count:
            updated_post['_id'] = post_id
            return json.loads(json_util.dumps(updated_post)), 200
        return {'error': 'Post not found'}, 404

    def delete(self, post_id):
        result = posts_collection.delete_one({'_id': ObjectId(post_id)})
        if result.deleted_count:
            return {'message': 'Post deleted'}, 200
        return {'error': 'Post not found'}, 404

    def edit(self, post_id):
        data = request.get_json()
        updated_fields = {} 
        if 'title' in data:
            updated_fields['title'] = data['title']
        if 'content' in data:
            updated_fields['content'] = data['content']
        if 'scale' in data:
            updated_fields['scale'] = data['scale']
        if updated_fields:
            result = posts_collection.update_one({'_id': ObjectId(post_id)}, {'$set': updated_fields})
            if result.matched_count:
                updated_post = posts_collection.find_one({'_id': ObjectId(post_id)})
                return json.loads(json_util.dumps(updated_post)), 200
            else:
                return {'error': 'Post not found'}, 404
        else:
            return {'error': 'No fields to update'}, 400

api.add_resource(PostList, '/posts')
api.add_resource(Post, '/posts/<string:post_id>')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
