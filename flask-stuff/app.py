from flask import Flask, flash, request, redirect, url_for

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
#from PIL import Image
import sys
import time
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'D:\git\hackNJIT'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


subscription_key = "d90f8bc8848845a1851f80da02ca8ab3"
endpoint = "https://image-recognizing.cognitiveservices.azure.com/"
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
remote_image_url = "https://images.immediate.co.uk/production/volatile/sites/30/2017/01/Bananas-218094b-scaled.jpg" #find a way to upload an image


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('upload_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/image')
def recognizeImage():
    
    #Detect Objects - remote
    #This example detects different kinds of objects with bounding boxes in a remote image.
    
    print("===== Detect Objects - remote =====")
    # Get URL image with different objects
    remote_image_url_objects = "https://images.immediate.co.uk/production/volatile/sites/30/2017/01/Bananas-218094b-scaled.jpg"
    # Call API with URL
    detect_objects_results_remote = computervision_client.detect_objects(remote_image_url_objects)

    # Print detected objects results with bounding boxes
    print("Detecting objects in remote image:")
    objects = []
    if len(detect_objects_results_remote.objects) == 0:
        print("No objects detected.")
    else:
        for object in detect_objects_results_remote.objects:
            objects += [str(object.object_property)]
        for object in objects:
            print(object)
    
    return objects[0]#"this was supposed to analyze an image"
