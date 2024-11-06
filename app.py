from flask import Flask, request, render_template, session, flash
from database_utils import connect_db
import random
from common_utils import error_handler
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def welcome():
    menu_items = []
   
    menu_items = [
       {"sensorId":'124124125152', "label": "Capteur 1", "itemType":'sensor', "data":{"temp":23, "humidity":45, "pressure":102, "air_quality":67}},
       {"sensorId":'124124125152', "label": "Capteur 2", "itemType":'sensor',"data":{"temp":26, "humidity":65}},
       {"sensorId":'1241121424125152', "label": "Capteur 3", "itemType":'sensor', "data":{"temp":34, "humidity":66, "pressure":102}},

    ]

    return render_template('startMenu.html', menu_items=menu_items)

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