
Working Link: https://visual-product-matcher-4154.onrender.com 



# Visual Product Matcher

![License](https://img.shields.io/badge/license-MIT-blue.svg) ![Build](https://img.shields.io/badge/build-passing-green.svg) ![Python](https://img.shields.io/badge/python-3.8+-blue.svg) ![Node.js](https://img.shields.io/badge/node-16+-green.svg) ![Status](https://img.shields.io/badge/status-active-success.svg) ![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)

A computer vision web application that allows users to find visually similar products from a database by uploading an image or providing an image URL. Powered by deep learning embeddings and efficient vector search.

## 📋 Table of Contents
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Usage Examples](#-usage-examples)
- [Configuration](#-configuration)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

## ✨ Key Features
* **Visual Similarity Search:** Utilizes deep learning (CNNs) to generate embeddings and match product aesthetics
* **Dual Input Methods:** Supports both local file uploads and direct image URLs
* **Smart Ranking:** Results are sorted by similarity score (Euclidean distance or Cosine similarity)
* **Fast Vector Search:** FAISS-powered similarity search for instant results
* **Metadata Management:** MongoDB integration for rich product information
* **Scalable Architecture:** Designed to handle large product databases efficiently
* **RESTful API:** Complete API for integration with other systems

## 🛠 Tech Stack

### Frontend
- **Framework:** React 18+
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios
- **Build Tool:** Webpack/Create React App

### Backend
- **Framework:** FastAPI or Flask (Python)
- **ML Libraries:** PyTorch / TensorFlow
- **Vector Database:** FAISS (Facebook AI Similarity Search)
- **Document Database:** MongoDB
- **Server:** Uvicorn (FastAPI) / Gunicorn (Flask)

### DevOps
- **Containerization:** Docker & Docker Compose
- **Version Control:** Git

## 📁 Project Structure

```
visual-product-matcher/
├── backend/
│   ├── app.py                 # Main FastAPI/Flask application
│   ├── requirements.txt        # Python dependencies
│   ├── models/
│   │   ├── embedding_model.py # CNN model for embeddings
│   │   └── product_model.py   # Data models
│   ├── routes/
│   │   ├── search.py          # Search endpoints
│   │   └── upload.py          # Upload endpoints
│   ├── services/
│   │   ├── faiss_service.py   # Vector search service
│   │   ├── mongodb_service.py # Database service
│   │   └── image_service.py   # Image processing
│   └── config.py              # Configuration settings
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── SearchForm.jsx
│   │   │   ├── ResultsGrid.jsx
│   │   │   └── ImageUpload.jsx
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── tailwind.config.js
├── docker-compose.yml         # Multi-container setup
├── .env.example               # Environment variables template
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker & Docker Compose (optional)
- MongoDB (local or cloud)

### Backend Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kakarot2003/visual-product-matcher.git
   cd visual-product-matcher
   ```

2. **Set up Python environment:**
   ```bash
   cd backend
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings (MongoDB URI, API keys, etc.)
   ```

5. **Start the backend server:**
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd ../frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Configure API endpoint:**
   ```bash
   # Create .env.local file
   echo "REACT_APP_API_URL=http://localhost:8000" > .env.local
   ```

4. **Start the development server:**
   ```bash
   npm start
   ```
   The application will open at `http://localhost:3000`

### Docker Setup (Optional)

```bash
docker-compose up -d
```

This will start:
- MongoDB on port 27017
- Backend API on port 8000
- Frontend on port 3000

## 📚 API Documentation

### Search Endpoint

**POST** `/api/search`

Search for visually similar products.

**Request:**
```json
{
  "image": "base64_encoded_image_or_file",
  "top_k": 10,
  "similarity_threshold": 0.5
}
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "product_id": "12345",
      "name": "Product Name",
      "similarity_score": 0.95,
      "image_url": "https://example.com/image.jpg",
      "price": 29.99,
      "category": "Electronics"
    }
  ],
  "execution_time_ms": 145
}
```

### Upload Product Endpoint

**POST** `/api/products/upload`

Add a new product to the database.

**Request:**
```json
{
  "name": "Product Name",
  "description": "Product description",
  "price": 29.99,
  "category": "Electronics",
  "image_url": "https://example.com/image.jpg"
}
```

**Response:**
```json
{
  "success": true,
  "product_id": "12345",
  "message": "Product added successfully"
}
```

### Search by URL Endpoint

**POST** `/api/search-by-url`

Search using an image URL instead of uploading.

**Request:**
```json
{
  "image_url": "https://example.com/product-image.jpg",
  "top_k": 10
}
```

**Response:** Same as Search Endpoint

### Health Check

**GET** `/api/health`

```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

## 💡 Usage Examples

### Example 1: Upload an Image and Search

```bash
curl -X POST "http://localhost:8000/api/search" \
  -F "image=@/path/to/image.jpg" \
  -H "Content-Type: multipart/form-data"
```

### Example 2: Search Using Image URL

```bash
curl -X POST "http://localhost:8000/api/search-by-url" \
  -H "Content-Type: application/json" \
  -d '{
    "image_url": "https://example.com/product.jpg",
    "top_k": 5
  }'
```

### Example 3: React Component Usage

```jsx
import React, { useState } from 'react';
import axios from 'axios';

export default function ProductSearch() {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (imageFile) => {
    setLoading(true);
    const formData = new FormData();
    formData.append('image', imageFile);
    formData.append('top_k', 10);

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_API_URL}/api/search`,
        formData
      );
      setResults(response.data.results);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input
        type="file"
        onChange={(e) => handleSearch(e.target.files[0])}
        accept="image/*"
      />
      {loading && <p>Searching...</p>}
      <div className="results-grid">
        {results.map((product) => (
          <div key={product.product_id} className="product-card">
            <img src={product.image_url} alt={product.name} />
            <h3>{product.name}</h3>
            <p>Similarity: {(product.similarity_score * 100).toFixed(2)}%</p>
            <p>${product.price}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# MongoDB
MONGODB_URI=mongodb://localhost:27017
DATABASE_NAME=visual_matcher

# API Settings
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=False

# FAISS Settings
FAISS_INDEX_PATH=./data/faiss_index.bin
EMBEDDING_DIMENSION=512

# Image Processing
MAX_IMAGE_SIZE=10485760  # 10MB in bytes
ALLOWED_EXTENSIONS=jpg,jpeg,png,gif

# CORS
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com

# Model Settings
MODEL_NAME=resnet50
PRETRAINED=true
```

### Model Configuration

Edit `backend/config.py` to customize:

```python
MODEL_CONFIG = {
    'architecture': 'resnet50',  # or 'vgg16', 'inception_v3'
    'pretrained': True,
    'embedding_dim': 512,
    'batch_size': 32,
    'device': 'cuda'  # or 'cpu'
}

FAISS_CONFIG = {
    'similarity_metric': 'cosine',  # or 'euclidean'
    'index_type': 'IVF',
    'nprobe': 10
}
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/visual-product-matcher.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

3. **Make your changes** and commit
   ```bash
   git commit -m 'Add amazing feature'
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

5. **Open a Pull Request**

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript/React
- Write tests for new features
- Update documentation as needed
- Keep commits atomic and descriptive

## 📄 License

Distributed under the MIT License. See `LICENSE` file for more information.

## 🆘 Support

For support, please:
- Open an [issue](https://github.com/kakarot2003/visual-product-matcher/issues)
- Check existing [discussions](https://github.com/kakarot2003/visual-product-matcher/discussions)
- Review the [documentation](https://github.com/kakarot2003/visual-product-matcher/wiki) (if available)

---
 
**Made by Ankit Raj 
