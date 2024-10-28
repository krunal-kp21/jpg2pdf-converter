from flask import Flask, request, render_template, send_file
from PIL import Image
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/convert', methods=['POST'])
def convert_image_to_pdf():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']

    # Check if the file is a JPG or JPEG image
    if file.filename == '' or not (file.filename.endswith('.jpg') or file.filename.endswith('.jpeg')):
        return "Please upload a JPG or JPEG image.", 400

    # Save the uploaded file
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(image_path)

    # Convert the image to PDF
    pdf_path = image_path.rsplit('.', 1)[0] + ".pdf"
    img = Image.open(image_path)
    img = img.convert("RGB")  # Ensure it's in RGB mode
    img.save(pdf_path, "PDF", resolution=100.0)

    # Serve the PDF file as a download
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
