from flask import Flask, request, jsonify
from dataclasses import dataclass
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80), nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(80), nullable=False)
	profile_picture = db.Column(db.String(200))
	status_message = db.Column(db.String(200))
	privacy_settings = db.Column(db.String(200))
	contacts = db.Column(db.String(200))
	groups = db.Column(db.String(200))

@app.route('/signup', methods=['POST'])
def signup():
	data = request.get_json()
	if User.query.filter_by(email=data.get('email')).first() is not None:
		return jsonify({'message': 'Email already in use'}), 400
	user = User(**data)
	db.session.add(user)
	db.session.commit()
	return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
	data = request.get_json()
	email = data.get('email')
	password = data.get('password')
	user = User.query.filter_by(email=email).first()
	if not user:
		return jsonify({'message': 'Email not found'}), 404
	if user.password != password:
		return jsonify({'message': 'Incorrect password'}), 401
	return jsonify({'message': 'Logged in successfully'}), 200

@app.route('/logout', methods=['POST'])
def logout():
	data = request.get_json()
	email = data.get('email')
	user = User.query.filter_by(email=email).first()
	if not user:
		return jsonify({'message': 'User not found'}), 404
	return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
	data = request.get_json()
	email = data.get('email')
	user = User.query.filter_by(email=email).first()
	if not user:
		return jsonify({'message': 'User not found'}), 404
	user.password = 'new_password'
	db.session.commit()
	return jsonify({'message': 'Password reset successfully'}), 200

if __name__ == '__main__':
	app.run(debug=True)