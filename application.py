from flask import Flask, request, render_template, send_from_directory, url_for, flash, redirect
import os
from werkzeug.utils import secure_filename
import base64

app = Flask(__name__)

UPLOAD_FOLDER = './'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

queue = []

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/upload-image', methods=['GET', 'POST'])
def upload_file():
    print(request.files)
    print(request.method)
    if request.method == "POST":
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # File is valid, save it
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            queue.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            os.system('python jeff.py ./' + filename)
            with open('./' + filename, 'rb') as img_file:
                img_data = base64.b64encode(img_file.read()).decode('utf-8')
            return render_template('index.html', img_data=img_data)
    return render_template('index.html')

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def play_music():


if __name__ == '__main__':
    app.secret_key = 'super secret key'

    app.debug = True
    app.run(host='127.0.0.1', port=8080)