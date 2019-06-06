import sched, time,datetime
#import RPi.GPIO as GPIO
import local
import cimis
import relay_motion
import threading

temperature = 0
humidity = 0
temp_avg = 0
hum_avg = 0
count = 0
cimis_count = 0

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
    print (start_time)
    t=threading.Thread(target=relay_motion.relay,args=(start_time,water_duration))
    t.start()
        


#get local temp and humidity and compare with CIMIS data every hour to calculate amount of water needed to water lawn
def read_sensors(current_hour):

    global temperature, humidity, temp_avg, hum_avg, count, cimis_count
    
    temperature, humidity = local.local_data()
    temp_avg += temperature
    hum_avg += humidity
    count=count+1
    print("TEMP SUM: %d HUM SUM: %d\n" %(temp_avg,hum_avg))
    
    new_hour = datetime.datetime.now().time().hour
    #current_hour = 12
    current_hour = 9
    new_hour = 10
    #new_hour = current_hour+1
    cimis_count = 2
    if (new_hour == current_hour+1):
        temp_avg = temp_avg/count
        hum_avg = hum_avg/count
        print("Temp Avg: %d Hum Avg: %d\n" %(temp_avg, hum_avg))
        
        if (cimis.cimis(current_hour*100)!=None):
            cimis_hr, cimis_eto, cimis_temp, cimis_hum = cimis.cimis(current_hour*100)
            print("CIMIS hr: %d eto: %f hum: %f" %(cimis_hr, cimis_eto, cimis_hum))
            if (cimis_count>0):
                missed_hours = cimis_count  
                print("CIMIS_Count = %d\n" %missed_hours)

                for i in range (cimis_count):
                    current_hour -= 1
                    cimis_hr1, cimis_eto1, cimis_temp1, cimis_hum1 = cimis.cimis(current_hour*100)
                    cimis_eto += cimis_eto1
                    print("Eto sum: %f\n" %cimis_eto)
                    cimis_temp += cimis_temp1
                    cimis_hum += cimis_hum1
                    print("TEMP SUM: %f HUM SUM: %f\n" %(cimis_temp, cimis_hum))
                
                print("MISSED HOURS: %d\n" %missed_hours)
                cimis_temp = cimis_temp / (missed_hours+1)
                cimis_hum = cimis_hum / (missed_hours+1)
                print("After missed: eto: %f temp: %f hum: %f\n" %(cimis_eto, cimis_temp, cimis_hum))

        else:
            #save hour not calculated
            cimis_count += 1

        new_et = derate(cimis_eto, cimis_hum, hum_avg, cimis_temp, temp_avg)
        
        temp_avg=0
        hum_avg=0
        count=0

        water = water_needed(new_et)
        #water = 372
        print(water)
        
        duration = water_duration(water)
        print(duration)
        water_lawn(duration)



