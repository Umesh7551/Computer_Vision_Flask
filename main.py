# Import necessary modules
import os
import time
from datetime import datetime
from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import pymysql
import subprocess
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed, FileSize
from werkzeug.utils import secure_filename
import cv2
import io
import ffmpeg
# from flask_uploads import UploadSet, configure_uploads, IMAGES, TEXT
# from werkzeug.utils import secure_filename
# create an instance of Flask
app = Flask(__name__)

# Database Configuration
app.secret_key = 'computer_vision_secret_key'  # Replace with your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/computer_vision_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_EXTENSIONS'] = ['mp4', 'MP4']
# Create a directory for storing frames
captured_images = os.path.join(os.getcwd(), "captured_images")
os.makedirs(captured_images, exist_ok=True)
app.config['UPLOAD_FOLDER'] = captured_images
# app.config['UPLOADED_FILES_DEST'] = 'uploads'  # Store uploaded files in the 'uploads' folder
# configure_extensions(app)
# text_files = UploadSet('text', TEXT)  # Define the allowed file type(s)

# Create an instance of SQLAlchemy using app object
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=True, unique=True)
    password = db.Column(db.String(100), nullable=True)
    firstname = db.Column(db.String(100), nullable=True)
    lastname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True, unique=True)
    phone = db.Column(db.String(10), nullable=True)

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100), nullable=True)
    product_id = db.Column(db.String(100), nullable=True)
    date_time = db.Column(db.DateTime, default=datetime.utcnow())
    product_video = db.Column(db.LargeBinary)

def __init__(self, product_name, product_id, date_time, product_video):
   self.product_name = product_name
   self.product_id = product_id
   self.date_time = date_time
   self.product_video = product_video


class AddProductForm(FlaskForm):
    product_name = StringField('Product Name:  ', validators=[DataRequired()])
    product_id = StringField('Product Id:  ', validators=[DataRequired()])
    product_video = FileField('Select Video File:  ', validators=[FileRequired(), FileAllowed(['mp4', 'MP4'], 'Only video files are allowed.'),
        FileSize(max_size=1024 * 1024 * 2, message='File size must be less than 2MB.')  # Adjust the size limit as needed.
    ])
    submit = SubmitField('Submit')

class CaptureImage(FlaskForm):
    image = FileField('Select Image File', validators=[FileRequired(), FileAllowed(['jpeg', 'jpg'])])
    submit = SubmitField('Submit')


class LiveDetection(FlaskForm):
    submit = SubmitField('Live Detetion')

# Your product table (you can use a database like SQLAlchemy for a real application)
products = []

@app.route('/home/')
def home():
    return render_template('home.html')

# Function to convert video data into image frames
# def convert_video_to_frames(video_data, product_id):
#     # Create a directory for storing frames
#     frames_dir = os.path.join(os.getcwd(), "images")
#     os.makedirs(frames_dir, exist_ok=True)
#
#     # # Create a temporary video file to write video data
#     # temp_video_file = os.path.join(frames_dir, 'temp_video.mp4')
#
#     # Assuming 'video_blob' contains your MP4 video blob as bytes
#     video_bytes = io.BytesIO(video_data)
#     # with open(temp_video_file, 'wb') as temp_file:
#     #     temp_file.write(video_data)
#     # Write the bytes to a temporary file
#     with open('temp_video.mp4', 'wb') as temp_file:
#         temp_file.write(video_bytes.read())
#
#         # Open the video file using OpenCV
#         cap = cv2.VideoCapture(os.getcwd() + f"{temp_file}")
#         # cap = cv2.VideoCapture(os.getcwd() + temp_file)
#         frame_count = 0
#
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#
#         # Save the frame as an image in the frames directory
#         frame_filename = os.path.join(frames_dir, f"{product_id}_{frame_count:04d}.jpeg")
#         cv2.imwrite(frame_filename, frame)
#         frame_count += 1
#
#     cap.release()
def convert_video_to_frames(video_data, product_id):
    # Create a directory for storing frames
    frames_dir = os.path.join(os.getcwd(), "images")
    os.makedirs(frames_dir, exist_ok=True)

    # Create a temporary video file to write video data
    temp_video_file = os.path.join(os.getcwd(),'temp_video.mp4')

    # Write the bytes to a temporary video file
    with open(temp_video_file, 'wb') as temp_file:
        temp_file.write(video_data)

    # Open the video file using OpenCV
    cap = cv2.VideoCapture(temp_video_file)  # Use the temporary video file as the source

    if not cap.isOpened():
        print("Error: Video file not opened")
        return

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize the frame to the desired frame size
        frame = cv2.resize(frame, (384, 512))

        # Save the frame as an image in the frames directory
        frame_filename = os.path.join(frames_dir, f"{product_id}_{frame_count:04d}.jpeg")
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    cap.release()
    #cv2.destroyAllWindows()

@app.route('/')
@app.route('/index/', methods=['GET', 'POST'])
def index():
    form = AddProductForm()

    if form.validate_on_submit():
        product_name = form.product_name.data
        product_id = form.product_id.data
        product_video = form.product_video.data
        # Save the uploaded file with a unique filename
        filename = secure_filename(product_video.filename)
        # product_video.save(os.path.join(
        #     app.instance_path, 'uploads', filename
        # ))
        # print(product_video)
        # file_path = os.path.join(app.config['UPLOADED_FILES_DEST'], product_video.filename)
        # product_video.save(file_path)
        # print(product_video)
        # with open(product_video.filename, 'rb') as video_file:
        #     video_data = video_file.read()
        # # print(video_data)

        if product_video:
            video_data = product_video.read()
            # print(video_data)


        # product = Products(product_name, product_id, datetime.utcnow(), product_video)
            product = Products(
                product_name=product_name,
                product_id=product_id,
                date_time=datetime.utcnow(),
                product_video=video_data  # Assuming 'filename' is the path to the saved video file.
            )
        # product = {'product_name': product_name, 'product_id': product_id, 'date_time': datetime.utcnow(), 'product_video': file_path}
        # products.append(product)
            db.session.add(product)
            db.session.commit()


            # Convert the video to frames and save them
            convert_video_to_frames(video_data, product_id)
            # Don't forget to close the file after you're done with it
            product_video.close()
        # Redirect to the home page to see the updated table
        return redirect(url_for('home'))

    return render_template('index.html', form=form)


@app.route('/settings')
def settings():
    return render_template("settings.html")


@app.route('/labelling', methods=['POST'])
def labelling():
    # Place the code here to execute your test-label.py script
    # You can use the subprocess module to run the Python script

    subprocess.run(["python", "test_label.py"])
    return 'Labelling script executed'


@app.route('/training', methods=['POST'])
def training():
    # Place the code here to execute your test-label.py script
    # You can use the subprocess module to run the Python script

    subprocess.run(["python", "training.py"])
    return 'Training script executed'

@app.route('/conversion', methods=['POST'])
def conversion():
    # Place the code here to execute your test-label.py script
    # You can use the subprocess module to run the Python script

    subprocess.run(["python", "export.py"])
    return 'Conversion script executed'


@app.route('/detection', methods=['POST'])
def detection():
    # Place the code here to execute your test-label.py script
    # You can use the subprocess module to run the Python script

    subprocess.run(["python", "detect.py"])
    return 'Detection script executed'

@app.route('/prediction', methods=['POST'])
def prediction():
    # Place the code here to execute your test-label.py script
    # You can use the subprocess module to run the Python script

    subprocess.run(["python", "detect.py"])
    return 'Prediction script executed'

@app.route('/pushtoS3', methods=['POST'])
def pushtos3():
    # Place the code here to execute your test-label.py script
    # You can use the subprocess module to run the Python script

    subprocess.run(["python", "pushtos3.py"])
    return 'Push to S3 script executed'

def delete_all_files_in_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file: {e}")

@app.route('/capture_image', methods=['GET','POST'])
def capture_image():
    form = CaptureImage()
    if request.method == 'POST' and form.validate_on_submit():
        image = form.image.data
        if image:
            # Delete all existing files in the upload folder
            delete_all_files_in_folder(app.config['UPLOAD_FOLDER'])
            # Save the uploaded file with a unique filename
            filename = secure_filename(image.filename)
            if filename:
                destination = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(destination)
                time.sleep(1.5)
                prediction()

                # # Optionally, you can store the file path in a database
                # # Here, we'll just return the uploaded file's URL
                return redirect(url_for('uploaded_file', filename=filename))
    return render_template("capture_image.html", form=form)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # You can provide a link to the uploaded file
    return f'Success! You can access the uploaded file <a href="{url_for("static", filename=filename)}">{filename}</a>.'


@app.route('/live_detection', methods=['GET', 'POST'])
def live_detection():
    video_capture = cv2.VideoCapture(0)
    return render_template('live_detection.html', video_capture=video_capture)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=7551)


