from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import datetime
from flask import *
app = Flask(__name__)

import sqlite3
conn=sqlite3.connect('../sensorsData.db')
curs=conn.cursor()

# Retrieve LAST data from database
def getLastData():
	for row in curs.execute("SELECT * FROM SONIC_data ORDER BY timestamp DESC LIMIT 1"):
		time = str(row[0])
		dist = row[1]
	#conn.close()
	return time, dist


def getHistData (numSamples):
	curs.execute("SELECT * FROM SONIC_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
	data = curs.fetchall()
	dates = []
	dist = []
	for row in reversed(data):
		dates.append(row[0])
		dist.append(row[1])
	return dates, dist

# Test data for cleanning possible "out of range" values
def testeData(dist):
	n = len(dist)
	for i in range(0, n-1):
		if (dist[i] < 10 or dist[i] >80):
			dist[i] = dist[i-2]
	return dist	

def maxRowsTable():
	for row in curs.execute("select COUNT(dist) from  SONIC_data"):
		maxNumberRows=row[0]
	return maxNumberRows

#initialize global variables	
def freqSample():
	times, dist = getHistData (2)
	fmt = '%Y-%m-%d %H:%M:%S'
	tstamp0 = datetime.strptime(times[0], fmt)
	tstamp1 = datetime.strptime(times[1], fmt)
	freq = tstamp1-tstamp0
	freq = int(round(freq.total_seconds()/60))
	return (freq)	



# define and initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 101):
        numSamples = 100

global freqSamples
freqSamples = freqSample()

global rangeTime
rangeTime = 100	

# main route 
@app.route("/")
def index():
	
	time, dist = getLastData()
	templateData = {
	  'time'		: time,
      'dist'		: dist,
      'numSamples'	: numSamples
	}
	return render_template('index.html', **templateData)



@app.route('/', methods=['POST'])
def my_form_post():
    global numSamples 
    global freqSamples
    global rangeTime
    rangeTime = int (request.form['rangeTime'])
    if (rangeTime < freqSamples):
        rangeTime = freqSamples + 1
    numSamples = rangeTime//freqSamples
    numMaxSamples = maxRowsTable()
    if (numSamples > numMaxSamples):
        numSamples = (numMaxSamples-1)
    
    time, dist = getLastData()
    
    templateData = {
	  'time'		: time,
      'dist'		: dist,
      'freq'		: freqSamples,
      'rangeTime'	: rangeTime
	}
    return render_template('index.html', **templateData)
	
	
@app.route('/plot/dist')
def plot_dist():
	times, dist = getHistData(numSamples)
	ys = dist
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