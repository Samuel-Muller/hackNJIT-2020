from flask import Flask, flash, request, redirect, url_for

from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
#import matplotlib.pyplot as plt #having some trouble with installing matplotlib
from io import BytesIO

from array import array
import os
from PIL import Image
import sys
import time
from werkzeug.utils import secure_filename
import requests

UPLOAD_FOLDER = 'D:\git\hackNJIT\\uploads'
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
            return redirect(url_for('image',
                                    filename=filename))
    return '''
    <!doctype html>
    <body style="background-color:lightgray;">
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
        </form>
    </body>
    '''

@app.route('/image')
def image():
    
    filename = request.args.get('filename')
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    analyze_url = endpoint + "vision/v3.1/analyze"


    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Objects'}
    response = requests.post(
        analyze_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()

    # The 'analysis' object contains various fields that describe the image. The most
    # relevant caption for the image is obtained from the 'description' property.
    analysis = response.json()
    print(analysis)
    #image_caption = analysis["description"]["captions"][0]["text"].capitalize()
    objects = analysis["objects"]

    return '''
    <!doctype html>
    <body style="background-color:lightgray;">
        <title>Image data:</title>
        <h1>Image data:</h1>
        ''' + str(analysis) + '''
        <br>
        <br>
        <h3>Currency converter:</h3>
        <iframe width="175" height="202" id="themoneyconverter-mini" src="https://themoneyconverter.com/MoneyConverter?from=EUR&amp;to=USD" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" seamless="seamless"></iframe>
    </body>
    '''



'''
    print("===== Detect Objects - remote =====")
    # Get URL image with different objects
    remote_image_url_objects = image_path #"https://images.immediate.co.uk/production/volatile/sites/30/2017/01/Bananas-218094b-scaled.jpg"
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
    
    return objects[0]#"this was supposed to analyze an image"'''
