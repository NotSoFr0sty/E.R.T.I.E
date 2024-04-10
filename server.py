from flask import Flask, render_template, request
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    # return render_template('index.html') #TODO: use this line after testing render
    return render_template('render.html')
    # return app.send_static_file('render.html')

# @app.route('/select-floor-plan')


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)