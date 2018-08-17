import os

from werkzeug import secure_filename
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

from cheese import SrtParser
from cheese import SmiParser


UPLOAD_FOLDER = '/Users/Sdalbsoo/workspace/python-projects/cheese/files'
ALLOWED_EXTENSIONS = set(['srt', 'smi'])


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/subtitle_dictionary")
def subtitle_dictionary():
    subtitle_path = request.args.get("path", None)
    word_meanings = None
    if subtitle_path is not None:
        srt = SrtParser(subtitle_path)
        sentences = srt.extract_sentences()
        extracted_words = srt.extract_words(sentences)
        word_meanings = srt.dict_parser.searchdict(extracted_words)
    return render_template(
        "subtitle.html",
        path=subtitle_path,
        word_meanings=word_meanings,
    )


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            return redirect(url_for('subtitle_dictionary', path=path))
        else:
            return "Now allowed file"
    else:
        return "Something Wrong"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
