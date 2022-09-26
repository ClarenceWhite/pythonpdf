import os
import shutil
from flask import Flask, render_template,send_from_directory,abort, request, redirect, url_for
from main import PdfMerger

app = Flask(__name__)
merger = PdfMerger('en.pdf', 'cn.pdf', 'en_split', 'cn_split')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploaded')
def uploaded():
    return render_template('uploaded.html')

@app.route('/merged')
def merged():
    return render_template('merged.html')

@app.route('/error')
def error():
    return render_template('error.html')

@app.route('/', methods=['POST'])
def upload_file():
    merger.cleanup()
    valid_names = ['en.pdf', 'cn.pdf']
    for uploaded_file in request.files.getlist('pdf_file'):
        if uploaded_file.filename in valid_names and len(request.files.getlist('pdf_file')) == 2:
            uploaded_file.save(uploaded_file.filename)
        else:
            return redirect(url_for('error'))
    return redirect(url_for('uploaded'))

@app.route('/merge')
def merge():
    merger.split_pdf(file_name=merger.en_file, folder_name=merger.en_split)
    merger.split_pdf(file_name=merger.cn_file, folder_name=merger.cn_split)
    merger.merge_pdf(en_folder=merger.en_split, cn_folder=merger.cn_split)
    merger.remove_redundancy()
    merger.compress()
    if "merged-compressed.pdf" in os.listdir():
        return redirect(url_for('merged'))
    else:
        return redirect(url_for('error'))

DOWNLOAD_DIRECTORY = os.getcwd()
@app.route('/download/<path:path>', methods = ['GET','POST'])
def return_files(path):
    """Download a file."""
    try:
        return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=True)
    except FileNotFoundError:
        abort(404)


if __name__ =="__main__":
    app.run(host='0.0.0.0', port = 8000, threaded = True, debug = True)

