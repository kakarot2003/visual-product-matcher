import os
import json
import math
import requests
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from PIL import Image  # <--- Works on all Python versions

app = Flask(__name__)

# --- CONFIGURATION ---
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- THE "VISUAL BRAIN" (Color Fingerprint Algorithm) ---
def get_image_fingerprint(image_path):
    """
    Creates a numerical 'fingerprint' for an image based on color.
    """
    try:
        img = Image.open(image_path).convert('RGB')
        img = img.resize((16, 16), Image.Resampling.LANCZOS)
        pixels = list(img.getdata())
        return pixels
    except Exception as e:
        print(f"Error processing image: {e}")
        return []

def calculate_similarity(fingerprint1, fingerprint2):
    """
    Compares two fingerprints using Euclidean Distance.
    """
    if not fingerprint1 or not fingerprint2:
        return 0
    
    diff = 0
    for p1, p2 in zip(fingerprint1, fingerprint2):
        diff += (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 + (p1[2] - p2[2])**2
    
    mse = diff / (len(fingerprint1) * 3)
    rmse = math.sqrt(mse)
    
    return round(100 - (rmse / 255.0 * 100), 2)

# --- DATABASE LOGIC ---
def get_similar_products(query_img_path):
    user_fingerprint = get_image_fingerprint(query_img_path)
    
    with open('products.json', 'r') as f:
        products = json.load(f)
    
    scored_products = []

    for product in products:
        try:
            # Download DB image to temp if needed
            db_img_name = f"temp_{product['id']}.jpg"
            db_img_path = os.path.join(app.config['UPLOAD_FOLDER'], db_img_name)
            
            if not os.path.exists(db_img_path):
                try:
                    r = requests.get(product['image_url'], timeout=5)
                    with open(db_img_path, 'wb') as f:
                        f.write(r.content)
                except:
                    continue # Skip if download fails
            
            db_fingerprint = get_image_fingerprint(db_img_path)
            score = calculate_similarity(user_fingerprint, db_fingerprint)
            
            product['score'] = score
            scored_products.append(product)
            
        except Exception as e:
            continue

    scored_products.sort(key=lambda x: x['score'], reverse=True)
    return scored_products[:3]

# --- ROUTES ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files: return jsonify({'error': 'No file'}), 400
    file = request.files['file']
    
    if file.filename:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        matches = get_similar_products(filepath)
        return jsonify({'uploaded_image': filepath, 'matches': matches})
    return jsonify({'error': 'No filename'}), 400

@app.route('/upload-url', methods=['POST'])
def upload_url():
    data = request.json
    if not data or 'url' not in data: return jsonify({'error': 'No URL'}), 400
    
    try:
        response = requests.get(data['url'], timeout=5)
        filename = "url_upload.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
            
        matches = get_similar_products(filepath)
        return jsonify({'uploaded_image': filepath, 'matches': matches})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)