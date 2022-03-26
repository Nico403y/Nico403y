import time
import sqlite3
import RPi.GPIO as GPIO
import schedule
from w1thermsensor import W1ThermSensor

dbname='sensorsData.db'
sensor = W1ThermSensor()

TRIG = 16
ECHO = 18

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)


print ("Waiting For Sensor To Settle")
time.sleep(1) #settling time 

# get data from Sonic sensor
def getSONICdata ():	
    dist_add = 0
    k=0
    for x in range(20):
        try:
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO)==0:
                pulse_start = time.time()

            while GPIO.input(ECHO)==1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            
            distance = pulse_duration * 17150

            distance = round(distance, 3)
            print (x, "distance: ", distance)
        
            dist_add = dist_add + distance
            #print "dist_add: ", dist_add
            time.sleep(.1) # 100ms interval between readings
        
        except Exception as e: 
        
            pass
    
    
    print ("x: ", x+1)
    print ("k: ", k)

    avg_dist=dist_add/(x+1 -k)
    dist=round(avg_dist,3)
    #print ("dist: ", dist)
    return dist

# get data from weather sensor
def getTemp ():
    while True:
        temp = sensor.get_temperature()
        print("The temperature is %s celsius" % temp)
        time.sleep(1)
        return temp

# log sensor data on database
def logData (dist):
	
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	
	curs.execute("INSERT INTO SONIC_data values(datetime('now'), (?))", (dist))
	conn.commit()
	conn.close()

def logDataTemp (temp):
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	
	curs.execute("INSERT INTO dsb_data values(datetime('now'), (?))", (temp))
	conn.commit()
	conn.close()


# main function
def main():
    dist = getSONICdata()
    temp = getTemp()
    logData(dist)
    logDataTemp(temp)

# ------------ Execute program 
schedule.every(30).minutes.do(main)

while True:
    schedule.run_pending()
    time.sleep(1)