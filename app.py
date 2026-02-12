import os
import json
import random
import requests  # <--- NEW IMPORT
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max limit

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def load_products():
    with open('products.json', 'r') as f:
        return json.load(f)

def get_matches():
    """Helper function to get random matches"""
    products = load_products()
    results = random.sample(products, k=min(len(products), 3))
    for p in results:
        p['score'] = random.randint(70, 99)
    results.sort(key=lambda x: x['score'], reverse=True)
    return results

@app.route('/')
def index():
    return render_template('index.html')

# --- EXISTING FILE UPLOAD ---
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            'uploaded_image': filepath,
            'matches': get_matches()
        })

# --- NEW URL UPLOAD FEATURE ---
@app.route('/upload-url', methods=['POST'])
def upload_url():
    data = request.json
    image_url = data.get('url')

    if not image_url:
        return jsonify({'error': 'No URL provided'}), 400

    try:
        # Download the image
        response = requests.get(image_url)
        if response.status_code == 200:
            filename = "url_upload.jpg"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)

            return jsonify({
                'uploaded_image': filepath,
                'matches': get_matches()
            })
        else:
            return jsonify({'error': 'Could not download image'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)