from flask import Flask, render_template, request, redirect
from waitress import serve
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import os
import cv2 as cv
from Modules.One_ImageProcessing.ImageProcessing import processFloorPlan
from Modules.Two_2Dto3D.my2Dto3D import convertTo3D
from Modules.Three_Pathfinding.v1 import calculatePath

app = Flask(__name__)
app.config['SECRET_KEY'] = 'NotSoFr0sty'
app.config['UPLOAD_FOLDER'] = 'static/floor-plans'

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload Floor Plan")

@app.route('/')
@app.route('/home')
@app.route('/index')
def index():

    return render_template('index.html')
    # return render_template('render.html')

@app.route('/select-floor-plan')
def selectFloorPlan():

    locDict = {
        "1": "House 1",
        "2": "House 2",
        "3": "House 3",
        "4": "Shopping Mall",
        "upload": "Custom Floor Plan"
    }
    locIndex = request.args.get('location')
    if locIndex == None:
        return redirect('/index')
    location = locDict[locIndex]

    if (locIndex=='upload'):
        return redirect('/upload-floor-plan')
    
    return render_template('select-floor-plan.html', locIndex=locIndex, location=location)

@app.route('/upload-floor-plan', methods=['GET', 'POST'])
def uploadFloorPlan():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        file.filename = 'upload.jpg'
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        # os.rename(f'./static/floor-plans/{file.filename}', 'upload.jpg') # secretly rename the file
        # return f"{file.filename} has been uploaded."
        return render_template('select-floor-plan.html', locIndex='upload', location='Custom Floor Plan')
    
    return render_template("upload-floor-plan.html", form=form)

@app.route('/render')
def createModel():
    if (int(request.args.get('pathFound'))): # If pathFound is true, then no need to create the model again.
        goal = [int(request.args.get('goalX')), int(request.args.get('goalY'))]
        start = [int(request.args.get('startX')), int(request.args.get('startY'))]
        locIndex = request.args.get('location')
        calculatePath(goal, start, locIndex)
        return render_template('render.html', locIndex=locIndex)
    
    # For generating model
    locIndex = request.args.get('location')
    processedImage = processFloorPlan(f'static/floor-plans/{locIndex}.jpg')
    convertTo3D(processedImage)
    return render_template('render.html', locIndex=locIndex)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)