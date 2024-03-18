from flask import Flask, request, jsonify
from dataclasses import dataclass
import jwt

app = Flask(__name__)

# Mock database
users = {}
posts = {}

@dataclass
class User:
	username: str
	email: str
	password: str
	profile: dict

@dataclass
class Post:
	user: str
	content: str
	likes: int
	retweets: int
	replies: list

@app.route('/register', methods=['POST'])
def register():
	data = request.get_json()
	username = data['username']
	email = data['email']
	password = data['password']
	if username in users:
		return jsonify({'message': 'Username already exists'}), 400
	users[username] = User(username, email, password, {})
	return jsonify({'message': 'User registered successfully'}), 200

@app.route('/login', methods=['POST'])
def login():
	data = request.get_json()
	username = data['username']
	password = data['password']
	if username not in users or users[username].password != password:
		return jsonify({'message': 'Invalid username or password'}), 400
	token = jwt.encode({'username': username}, 'secret', algorithm='HS256')
	return jsonify({'token': token}), 200

@app.route('/post', methods=['POST'])
def post():
	data = request.get_json()
	token = data.get('token')
	if not token:
		return jsonify({'message': 'Token is missing'}), 401
	try:
		decoded = jwt.decode(token, 'secret', algorithms=['HS256'])
	except:
		return jsonify({'message': 'Token is invalid'}), 401
	username = decoded['username']
	content = data.get('content')
	if not content:
		return jsonify({'message': 'Content is missing'}), 400
	if username not in users:
		return jsonify({'message': 'User not found'}), 404
	posts[len(posts)] = Post(username, content, 0, 0, [])
	return jsonify({'message': 'Post created successfully'}), 200

if __name__ == '__main__':
	app.run(debug=True)