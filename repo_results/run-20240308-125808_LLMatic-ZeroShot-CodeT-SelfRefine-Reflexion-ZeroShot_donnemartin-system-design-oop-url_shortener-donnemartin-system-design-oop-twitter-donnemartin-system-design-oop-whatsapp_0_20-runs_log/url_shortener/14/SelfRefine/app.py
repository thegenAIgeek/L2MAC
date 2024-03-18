from flask import Flask, request, jsonify, redirect
from dataclasses import dataclass
from datetime import datetime
import requests

app = Flask(__name__)

# Mock database
DB = {}

@dataclass
class URL:
	original: str
	shortened: str
	clicks: int
	click_data: list
	expiration: datetime

@app.route('/shorten', methods=['POST'])
def shorten_url():
	data = request.get_json()
	original_url = data.get('url')
	shortened_url = data.get('shortened')
	expiration = datetime.fromisoformat(data.get('expiration'))
	
	# Validate URL
	try:
		response = requests.get(original_url)
		response.raise_for_status()
	except (requests.RequestException, ValueError):
		return jsonify({'error': 'Invalid URL'}), 400
	
	# Check if shortened URL is available
	if shortened_url in DB:
		return jsonify({'error': 'Shortened URL already in use'}), 400
	
	# Create URL object and store in DB
	url = URL(original=original_url, shortened=shortened_url, clicks=0, click_data=[], expiration=expiration)
	DB[shortened_url] = url
	
	return jsonify({'message': 'URL shortened successfully', 'data': url}), 200

@app.route('/<shortened>', methods=['GET'])
def redirect_url(shortened):
	url = DB.get(shortened)
	
	# Check if URL exists
	if not url:
		return jsonify({'error': 'URL not found'}), 404
	
	# Check if URL has expired
	if datetime.now() > url.expiration:
		return jsonify({'error': 'URL has expired'}), 400
	
	# Increment click count and add click data
	url.clicks += 1
	url.click_data.append({'time': datetime.now().isoformat()})
	
	# Redirect to original URL
	return redirect(url.original, code=302)

@app.route('/analytics/<shortened>', methods=['GET'])
def get_analytics(shortened):
	url = DB.get(shortened)
	
	# Check if URL exists
	if not url:
		return jsonify({'error': 'URL not found'}), 404
	
	# Return analytics data
	return jsonify({'data': url}), 200

if __name__ == '__main__':
	app.run(debug=True)