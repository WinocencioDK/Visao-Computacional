from flask import Flask, render_template
app = Flask(__name__)

@app.route('/envio')
def index():
    return render_template('envioImagem.html')

@app.route('/resposta')
def resposta():
    return render_template('resposta.html')

