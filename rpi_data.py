import sched, time,datetime
#import RPi.GPIO as GPIO
import local
import cimis2
import relay_motion

rpi_update = sched.scheduler(time.time, time.sleep)
test_update = sched.scheduler(time.time, time.sleep)
temperature = 0
humidity = 0
temp_avg = 0
hum_avg = 0
count = 0

# Derate the ET
def derate(cimis_et, cimis_hum, gpi_hum, cimis_temp, gpi_temp):
    derated_et = cimis_et * (gpi_hum / cimis_hum) * (cimis_temp / gpi_temp)
    return derated_et

# Calculate the amount of water needed using the derated ET
def water_needed(derated_et):
    pf = 1.0
    sf = 200
    ie = 0.75
    water = (derated_et * pf * sf * 0.62) / ie
    return water

def water_duration(water):
    water_hr = water/1020
    water_min = water_hr*60
    return water_min

# Turn on the relay until the entire law is watered at a rate of 1020 gallons per hour or interrupted by nearby person
def water_lawn(water_duration):
    start_time = time.time()

    while ((time.time()-start_time) < water_duration):
        relay_motion.relay()
        



def read_sensors(current_hour):

    global temperature, humidity, temp_avg, hum_avg, count
    
    temperature, humidity = local.local_data()
    temp_avg += temperature
    hum_avg += humidity
    count=count+1
    print("TEMP SUM: %d HUM SUM: %d\n" %(temp_avg,hum_avg))
    new_hour = datetime.datetime.now().time().hour
    new_hour = current_hour+1
        #print("Temp Avg: %d Hum Avg: %d\n" %(temp_avg, hum_avg))
        #cimis_hr, cimis_local, cimis_hum = cimis()
        #print("CIMIS hr: %d eto: %f hum: %f" %(cimis_hr, cimis_local, cimis_hum))
    if (new_hour == current_hour+1):
        temp_avg = temp_avg/count
        hum_avg = hum_avg/count
        print("Temp Avg: %d Hum Avg: %d\n" %(temp_avg, hum_avg))
        cimis_hr, cimis_eto, cimis_temp, cimis_hum = cimis2.cimis()
        print("CIMIS hr: %d eto: %f hum: %f" %(cimis_hr, cimis_eto, cimis_hum))
        #compute temp and humidity averages 
        #compare with CIMIS data
        new_et = derate(cimis_eto, cimis_hum, hum_avg, cimis_temp, temp_avg)
        temp_avg=0
        hum_avg=0
        count=0
        water = water_needed(new_et)
        water = 372
        print(water)
        duration = water_duration(water)
        print(duration)
        water_lawn(duration)
        #this_hour = datetime.datetime.now().time().hour
        

    
        # read from humidity sensor
        # read from thermistor
        # update hourly avg
        # display values on lcd
        # decide whether to turn on relay
        #print (time.time())



