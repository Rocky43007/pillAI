# app.py
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from color_detect import AIProcessor_Color
from shape_detect import AIProcessor_Shape
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/process_image', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return jsonify(error='No file part'), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify(error='No selected file'), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print("Filename: ", filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        shape_result = AIProcessor_Shape.detect_shape(filepath)
        color_result = AIProcessor_Color.get_color(filepath, 'thresh.png')
        response = {
            'color': color_result,
            'shape': shape_result
        }

        print(response)

        return jsonify(response), 200

    return jsonify(error='Invalid file format'), 400

@app.route('/hello', methods=['GET'])
def hello():
    return jsonify(message='Hello, world!'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
