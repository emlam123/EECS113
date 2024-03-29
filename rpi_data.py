import time,datetime
#import RPi.GPIO as GPIO
import local
import cimis
import relay_motion
import threading
import I2C_LCD_driver
import buzzer
import csv 

temperature = 0
humidity = 0
temp_avg = 0
hum_avg = 0
cimis_count = 0
temperatures=[]
humidities=[]
mutex = threading.Lock()
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
def water_lawn(water_duration,mylcd,mutex):
    start_time = time.time()
    t=threading.Thread(target=relay_motion.relay,args=(start_time,water_duration,mylcd,mutex,))
    t.start()
        


#get local temp and humidity and compare with CIMIS data every hour to calculate amount of water needed to water lawn
def read_sensors(current_hour,mylcd):


    global mutex,temperatures,humidities,temperature, humidity, temp_avg, hum_avg, count, cimis_count
    print("CURRENT HR: %d\n" %current_hour)

    temperatures = [None]*24
    humidities = [None]*24
    
    #current_hour = 14
    #temperatures[15] = 77
    #humidities[15] = 56
    #temperatures[14] = 73.4
    #humidities[14] = 54
    '''
    temperatures[9] = 75
    humidities[9] = 54
    temperatures[10]=77
    humidities[10]=56
    '''
    today = datetime.date.today()
    
    t=threading.Thread(target=local.local_data,args=(mylcd,temperatures,humidities,mutex,))
    t.start()
   
    #cimis_hr, cimis_eto, cimis_temp, cimis_hum = cimis.cimis(18*100,temperatures[18],humidities[18])
    #print("CIMIS hr: %d eto: %f hum: %f" %(cimis_hr, cimis_eto, cimis_hum))

    columns = [['Hour','Derated ET','Temperature','Humidity']]
    with open('data.csv','w') as f:
        writer = csv.writer(f)
        writer.writerow(columns)
    f.close()
   
    while (True):
        new_time = datetime.datetime.now().time()
        now = datetime.date.today()

        if ((new_time.hour > current_hour or now.day > today.day or now.month > today.month) and (new_time.minute==30 or new_time.minute==45 or new_time.minute==50)):
            buzzer.buzz()

            if (cimis.cimis(current_hour*100, temperatures[current_hour], humidities[current_hour])==None):
                print("Current hour:%d\n" %(current_hour))
                print("waiting\n")
                continue

            cimis_hr, cimis_eto, cimis_temp, cimis_hum = cimis.cimis(current_hour*100,temperatures[current_hour],humidities[current_hour])
            print("CIMIS hr: %d eto: %f hum: %f" %(cimis_hr, cimis_eto, cimis_hum))
            print(temperatures[current_hour],humidities[current_hour])

            new_et = derate(cimis_eto,cimis_hum,humidities[current_hour],cimis_temp,temperatures[current_hour])
            
            data = [[current_hour,new_et,temperatures[current_hour],humidities[current_hour]]]
            with open('data.csv','a') as f:
                writer = csv.writer(f)
                writer.writerow(data)
            f.close()

            current_hour += 1
            print("HOUR: %d\n" %current_hour)

            while(cimis.cimis(current_hour*100,temperatures[current_hour],humidities[current_hour])!=None):
                cimis_hr1, cimis_eto1, cimis_temp1, cimis_hum1 = cimis.cimis(current_hour*100, temperatures[current_hour], humidities[current_hour])
                print("cimis eto1:%f\n" %cimis_eto1)
                et = derate(cimis_eto1, cimis_hum, humidities[current_hour], cimis_temp, temperatures[current_hour])
                
                data = [[current_hour,et,temperatures[current_hour],humidities[current_hour]]]
                with open('data.csv','a') as f:
                    writer = csv.writer(f)
                    writer.writerow(data)
                f.close()
                
                new_et += et
                print("NEW ETO SUM: %f\n" %new_et)
                current_hour+=1
                cimis_count+=1
            
            
            print("MISSED HOURS: %d\n" %cimis_count)
            cimis_count = 0 
            print("CURRENT HOUR NEXT: %d\n" %current_hour) 
                    
            water = water_needed(new_et)
            print(water)
            
            duration = water_duration(water)
            print(duration)
            water_lawn(duration,mylcd,mutex)

