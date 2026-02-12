import os
import json
import random
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB file

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load product data
def load_products():
    with open('products.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

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
        
        # LOGIC: Here we simulate AI matching. 
        # In a real scenario, you'd use TensorFlow/PyTorch here.
        # For this assignment, we return random products to demonstrate the UI works.
        products = load_products()
        results = random.sample(products, k=3)
        
        # Add a fake "similarity score"
        for p in results:
            p['score'] = random.randint(70, 99)
            
        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return jsonify({
            'uploaded_image': filepath,
            'matches': results
        })

if __name__ == '__main__':
    app.run(debug=True)