from flask import Flask, flash, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
import os, requests
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

UPLOAD_FOLDER = 'static/results/'

app = Flask(__name__)
app.secret_key = os.environ.get("APP_SECRET_KEY")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def index():
    return render_template('subscription.html')

@app.route('/subscribe')
def subscribe():
    return render_template('register.html')

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
		data_id = request.form['data_id']
		audioFile = request.files['audioFile']
		print('audioFile', audioFile)
		filename = secure_filename(audioFile.filename) # save file 
		audioFilepath = os.path.join(app.instance_path, filename);
		audioFile.save(audioFilepath)

		imgFile = request.files['imgFile']
		print('imgFile', imgFile)
		filename = secure_filename(imgFile.filename) # save file 
		imgFilepath = os.path.join(app.instance_path, filename);
		imgFile.save(imgFilepath)

		outputFilename = f"merge-{data_id}.mp4"
		outputFilepath = UPLOAD_FOLDER + outputFilename

		try:
			response = requests.get(f"http://localhost:3000/wav2lip/{audioFile.filename}/{imgFile.filename}/{outputFilename}", timeout=5)
			response.raise_for_status()
			# Code here will only run if the request is successful
		except requests.exceptions.HTTPError as errh:
			print(errh)
		except requests.exceptions.ConnectionError as errc:
			print(errc)
		except requests.exceptions.Timeout as errt:
			print(errt)
		except requests.exceptions.RequestException as err:
			print(err)

		data, count = (supabase
		.table('files') 
		.insert({
			"audio_file": audioFilepath,
			"image_file": imgFilepath,
			"output_file": outputFilepath,
			"user_id": data_id})
		.execute())
		
		flash('Video successfully uploaded and displayed below')
		return render_template('mini-music-player.html', filename=outputFilename)
	else:
		print('args', request.args)
		print('files', request.files)

@app.route('/register', methods=['POST'])
def register():
    post_dict = request.form.to_dict()
    data, count = (supabase
    .table('users') 
    .insert(post_dict)
    .execute())
    data_dict = data[1]
    data_json = data_dict[0]
    data_id = data_json['id']
    return render_template('upload.html', data_id=data_id)

@app.route('/login', methods=['POST', 'GET'])
def login():
	if request.method == 'POST':
		print(request.form)
		user = request.form['nm']
		audiofile = request.files['audiofile']
		return redirect(url_for('success', name=user, audiofile=audiofile))
	else:
		user = request.args.get('nm')
		return redirect(url_for('success', name=user))


if __name__ == '__main__':
	app.run(debug=True)
