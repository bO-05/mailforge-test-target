from flask import Flask, request, send_file
import os
from docx_to_markdown import convert_docx_to_markdown

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return send_file('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'docxFile' not in request.files:
        return 'No file part', 400
    file = request.files['docxFile']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        docx_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(docx_path)
        md_path = os.path.join(UPLOAD_FOLDER, file.filename.replace('.docx', '.md'))
        convert_docx_to_markdown(docx_path, md_path)
        with open(md_path, 'r', encoding='utf-8') as md_file:
            md_content = md_file.read()
        return md_content

if __name__ == '__main__':
    app.run(debug=True)