from datetime import datetime
from keypad import keypad
import RPi.GPIO as GPIO
import time
import config
import requests
import json
"""
*** cURL equivalent *** 
    curl -H "Accept: application/json" https://et.water.ca.gov/api/data?appKey=APPKEY&targets=75&startDate=2019-05-30&endDate=2010-05-30&dataItems=day-asce-eto,hly-asce-eto

"""
target = '75'
def cimis(current_hr,emergency_temp,emergency_hum):
    print("IN CIMIS\n")
    # Requests data from today
    today = datetime.today().strftime('%Y-%m-%d')

    print("Zip code: %s" % target)

    headers = {
        'Accept': 'application/json',
    }

    params = (
        ('appKey', config.cimis_key),
        ('targets', target),
        ('startDate', today),
        ('endDate', today), 
        ('dataItems','day-asce-eto,hly-asce-eto,hly-rel-hum,hly-air-tmp')
    )

    response = requests.get('https://et.water.ca.gov/api/data', headers=headers, params=params)
    print(response.status_code)
    if (response.status_code!=200):
        return None
    
    try:
        data = response.json() # JSON format: https://et.water.ca.gov/Rest/Index 
    except ValueError:
        print("JSON DECODE ERROR\n")
        return None

    records = data["Data"]["Providers"][0]["Records"][1:] # skip first line, which is NoneType
    
    for record in records:
        eto = record.get("HlyAsceEto")
        humidity = record.get("HlyRelHum")
        temperature = record.get("HlyAirTmp")
        if (eto.get("Value") != None):
            if (int(record.get("Hour"))==current_hr):
                
                if (float(humidity.get("Value"))!=None):
                    humidity = float(humidity.get("Value"))

                else:
                    humidity = emergency_hum

                if (float(temperature.get("Value"))!=None):
                    temperature = float(temperature.get("Value"))
                
                else:
                    temperature=emergency_temp


                print("[%d] Et0: %.2f; Temp: %.2f Humidity: %.2f" % (int(record.get("Hour")), float(eto.get("Value")), temperature, humidity))
                return (int(record.get("Hour")), float(eto.get("Value")), temperature, humidity)

        else:
            return None



if __name__ == '__main__':

    ### KEYPAD INITIALIZATION ###
    kp = keypad(columnCount = 4)
    digit = None

    global target
    target = ""
    print("Enter your zip code or press '#' for Irvine: ")
    for i in range(5):
        digit = None
        while digit == None:
            digit = kp.getKey()
        if (digit == "#"):
            break;
        print(digit)
        target = target + str(digit)
        time.sleep(0.4)

    ### END KEYPAD ###
    current_hour=datetime.now().time().hour
    current_hour = (current_hour)*100
    if (cimis(current_hour)!=None):
        hr, eto, temp, hum = cimis(current_hour)
    else:
        #hour that wasn't recorded
        current_hour = current_hour
