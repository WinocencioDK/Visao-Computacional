import os , io
import urllib.request
import numpy as np
import cv2 as cv
from face import Face
from flask import Flask, render_template , flash, request
from google.cloud import vision
from werkzeug.utils import secure_filename
app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="client_secrets.json"
STATIC = '/home/willian/Documentos/Python Visao Computacional/Visao-Computacional/static/'
UPLOAD_FOLDER = '/home/willian/Documentos/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/envio')
def index():   
    return render_template('envioImagem.html')

@app.route('/renderImage' ,  methods=['POST'])
def renderImage():

    #Google Vision API
    client = vision.ImageAnnotatorClient()

    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))

        with io.open(UPLOAD_FOLDER + file.filename, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.face_detection(image=image)
        faces = response.face_annotations

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

        #OPEN CV
        face_classifier = cv.CascadeClassifier( cv.data.haarcascades +  'haarcascade_frontalface_default.xml')
        image = cv.imread(UPLOAD_FOLDER + file.filename)
        image_gray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(image_gray)
        for(x,y,w,h) in faces:
            cv.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)

        cv.imwrite(os.path.join(STATIC , file.filename), image)

    return render_template('resposta.html', rostos=rostos,imagem=file.filename)

if __name__ == '__main__':
    app.run(host='192.168.0.8', port=3001)
