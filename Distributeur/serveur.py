from flask import Flask, render_template, request
from setting.configProxy import getIp, getPort
import time
import os
app = Flask(__name__)

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    """Page for POST throught the site."""
    return render_template('form_submit.html')

@app.route('/sendcommand/', methods=['POST'])
def sendcommand():
    """Principal page for POST manually."""
    #command = request.form['command']
    command = request.get_json(force=True)
    print(command["sendcommand"])
    if(command["sendcommand"] == "retirerArgent"):
        moteurOn()
        time.sleep(5)
        moteurOff()
    return render_template('form_action.html', command=command)

def moteurOn():
    os.system("python /home/pi/Desktop/Distributeur/actions/Adafruit_Python_PCA9685/examples/moteurOn.py")

def moteurOff():
    os.system("python /home/pi/Desktop/Distributeur/actions/Adafruit_Python_PCA9685/examples/moteurOff.py")

# Run the app :)
if __name__ == '__main__':
    app.run(
        host=getIp(),
        port=getPort()
    )
