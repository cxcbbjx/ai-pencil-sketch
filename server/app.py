from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sketch_transform import convert_to_sketch
import os
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'static/sketches'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    filename = f"{uuid.uuid4().hex}.jpg"
    input_path = os.path.join(UPLOAD_FOLDER, 'input_' + filename)
    output_path = os.path.join(UPLOAD_FOLDER, 'output_' + filename)

    image.save(input_path)
    convert_to_sketch(input_path, output_path)

    return jsonify({'output_url': f'/sketches/output_{filename}'})

@app.route('/sketches/<filename>')
def get_sketch(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
