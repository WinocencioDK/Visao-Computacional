import os , io
import urllib.request
from face import Face
from flask import Flask, render_template , flash, request
from google.cloud import vision
from werkzeug.utils import secure_filename
app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="client_secrets.json"
UPLOAD_FOLDER = '/home/willian/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/envio')
def index():   
    return render_template('envioImagem.html')

@app.route('/renderImage' ,  methods=['POST'])
def renderImage():

    client = vision.ImageAnnotatorClient()

    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

        with io.open(UPLOAD_FOLDER + file.filename, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.face_detection(image=image)
        faces = response.face_annotations

        # Names of likelihood from google.cloud.vision.enums
        likelihood_name = ('DESCONHECIDO', 'MUITO_IMPROVAVEL', 'IMPROVAVEL', 'POSSIVEL',
                        'PROVAVEL', 'MUITO_PROVAVEL')
        
        
        rostos = []
        i = 1
        for face in faces:

            vertices = (['({},{})'.format(vertex.x, vertex.y)
            for vertex in face.bounding_poly.vertices])

            rosto = Face(i, likelihood_name[face.joy_likelihood], likelihood_name[face.sorrow_likelihood],likelihood_name[face.surprise_likelihood],likelihood_name[face.anger_likelihood],vertices)
            rostos.append(rosto)
            i = i + 1

    return render_template('resposta.html', rostos=rostos)

if __name__ == '__main__':
    app.run(host='192.168.0.8', port=3001)
