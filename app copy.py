import os
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, jsonify
from PIL import Image, ImageOps
from rembg import remove
import threading

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to remove the background from the image
def process_image(input_path, output_path):
    with open(input_path, 'rb') as input_file:
        input_data = input_file.read()
        output_data = remove(input_data)
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the about page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for the why page
@app.route('/why')
def why():
    return render_template('why.html')

# Route for the contact page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for handling file uploads
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'no-bg-' + filename)
        
        # Start a new thread to process the image in the background
        threading.Thread(target=process_image, args=(input_path, output_path)).start()
        
        # Redirect to the result route with the processed filename
        return redirect(url_for('result', filename='no-bg-' + filename))

# Route to display the result page
@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)

# Route to check the status of the processed image
@app.route('/status/<filename>')
def check_status(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return jsonify({'status': 'ready'})
    else:
        return jsonify({'status': 'processing'})

# Route for serving uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
