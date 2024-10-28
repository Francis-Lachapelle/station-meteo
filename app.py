from flask import Flask, request, render_template, session, flash
from database_utils import connect_db
import random
from common_utils import error_handler
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def welcome():
    return render_template('index.html')

#@app.route("/<string:device>")
#def show_device(device):
 #   return "<p>Hello, World!</p>"

@app.route("/update-section")
def show_device():
    random_number = random.randint(0, 50)
    return str(random_number)

if __name__ == '__main__':
    app.run(debug=True)

#https://flask.palletsprojects.com/en/3.0.x/patterns/javascript/