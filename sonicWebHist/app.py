from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import datetime
from flask import *
app = Flask(__name__)
import water_control

import sqlite3
conn=sqlite3.connect('../sensorsData.db')
curs=conn.cursor()

# Retrieve LAST data from database
def getLastData():
	for row in curs.execute("SELECT * FROM dsb_data ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[0])
		temp = row[1]
	#conn.close()
	return time, temp


def getHistData (numSamples):
	curs.execute("SELECT * FROM dsb_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	dates = []
	temp = []
	for row in reversed(data):
		dates.append(row[0])
		temp.append(row[1])
	return dates, temp

def maxRowsTable():
	for row in curs.execute("select COUNT(temp) from  dsb_data"):
		maxNumberRows=row[0]
	return maxNumberRows



# define and initialize global variables

# main route 
@app.route("/")
def index():
	
	time, temp = getLastData()
	templateData = {
	  'time'		: time,
      'temp'		: temp,
      'numSamples'	: numSamples
	}
	return render_template('index.html', **templateData)

@app.route('/index.html')
def activateBotton():
	water_control.water_control()
	print("test")


@app.route('/', methods=['POST'])
def my_form_post():
    global numSamples
    rangeTime = int (request.form['rangeTime'])
    numMaxSamples = maxRowsTable()
    if (numSamples > numMaxSamples):
        numSamples = (numMaxSamples-1)
    
    time = getLastData()
    
    templateData = {
	  'time'		: time,
      'rangeTime'	: rangeTime
	}
    return render_template('index.html', **templateData)
	
	
@app.route('/plot/temp')
def plot_dist():
	times, temp = getHistData(numSamples)
	ys = temp
	fig = Figure()
	axis = fig.add_subplot(1, 1, 1)
	axis.set_title("Water level [L]")
	axis.set_xlabel("Samples")
	axis.grid(True)
	xs = range(numSamples)
	axis.plot(xs, ys)
	canvas = FigureCanvas(fig)
	output = io.BytesIO()
	canvas.print_png(output)
	response = make_response(output.getvalue())
	response.mimetype = 'image/png'
	return response

if __name__ == "__main__":
	app.run(host='http://0.0.0.0', port=80, debug=False)