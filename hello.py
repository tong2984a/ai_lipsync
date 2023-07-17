from flask import Flask, flash, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
import os, inference_web

UPLOAD_FOLDER = 'static/results/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def index():
    return render_template('index.html')

@app.route('/success/<name>')
def success(name, audiofile):
	return 'welcome %s %s %s' % name, file, audiofile

@app.route('/display/<filename>')
def display_video(filename):
	print('display_video filename: ' + filename)
	return redirect(url_for(filename), code=301)

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		#   f = request.files['file']
		print('args', request.args)
		files_uploaded = request.files
		# files_uploaded = request.files.getlist('user_file_images')
		print('files_uploaded', files_uploaded)
		audioFile = files_uploaded.getlist('file1')
		imgFile = files_uploaded.getlist('file')
		print('audioFile', audioFile)
		print('imgFile', imgFile)

		audioFile = request.files['file1']
		filename = secure_filename(audioFile.filename) # save file 
		audioFilepath = os.path.join(app.instance_path, filename);
		audioFile.save(audioFilepath)

		imgFile = request.files['file']
		filename = secure_filename(imgFile.filename) # save file 
		imgFilepath = os.path.join(app.instance_path, filename);
		imgFile.save(imgFilepath)

		outputFilename = UPLOAD_FOLDER + 'result_voice.mp4'
		inference.makeFace(audioFilepath, imgFilepath, outputFilename)
		flash('Video successfully uploaded and displayed below')
		return render_template('index.html', filename=outputFilename)
	else:
		print('args', request.args)
		print('files', request.files)

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
###		print('user', user, 'file', file, 'audiofile', audiofile)
		print(request.form)
		user = request.form['nm']
###		file = request.files['file']
		audiofile = request.files['audiofile']
		return redirect(url_for('success', name=user, audiofile=audiofile))
	else:
		user = request.args.get('nm')
		return redirect(url_for('success', name=user))


if __name__ == '__main__':
	app.run(debug=True)
