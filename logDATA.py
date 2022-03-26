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
    try:
            sqliteConnection = sqlite3.connect(dbname)
            cursor = sqliteConnection.cursor()


            sqlite_insert_query = """INSERT INTO SONIC_data
                                (timestamp, dist) VALUES(datetime('now'), ?)"""
            tuple1 = (int(dist),)
            print("row værdi: ", tuple1)
            cursor.execute(sqlite_insert_query, tuple1)
            sqliteConnection.commit()
            print("Record inserted successfully into dbname, SONIC_data table ", cursor.rowcount)
            cursor.close()

    except sqlite3.Error as error:
            print("Failed to insert data into SONIC_data table", error)
    finally:
            if sqliteConnection:
                sqliteConnection.close()

def logDataTemp (temp):
    try:
        sqliteConnection = sqlite3.connect(dbname)
        cursor = sqliteConnection.cursor()


        sqlite_insert_query = """INSERT INTO dsb_data
                            (timestamp, temp) VALUES(datetime('now'), ?)"""
        tuple1 = (int(temp),)
        print("row værdi: ", tuple1)
        cursor.execute(sqlite_insert_query, tuple1)
        sqliteConnection.commit()
        print("Record inserted successfully into dbname, dsb_data table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
            print("Failed to insert data into SONIC_data table", error)
    finally:
            if sqliteConnection:
                sqliteConnection.close()

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