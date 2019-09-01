import os
import urllib.request
from flask import Flask, render_template , flash, request
from werkzeug.utils import secure_filename
app = Flask(__name__)

UPLOAD_FOLDER = '/home/willian'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/envio')
def index():
    return render_template('envioImagem.html')

@app.route('/renderImage' ,  methods=['POST'])
def renderImage():
    print("HELLO")

    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

    return render_template('resposta.html')

if __name__ == '__main__':
    app.run(host='192.168.0.8', port=3001)
