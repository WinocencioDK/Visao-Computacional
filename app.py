from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('envioImagem.html')

if __name__ == '__main__':
    app.run(host='192.168.0.8', port=3001)