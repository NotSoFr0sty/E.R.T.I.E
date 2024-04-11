from flask import Flask, render_template, request
from waitress import serve

app = Flask(__name__)

@app.route('/')
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
    location = locDict[locIndex]
    if (locIndex=='upload'):
        return render_template('upload-floor-plan.html', locIndex=locIndex, location=location)
    
    return render_template('select-floor-plan.html', locIndex=locIndex, location=location)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)