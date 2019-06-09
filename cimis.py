from datetime import datetime
import config
import requests

"""
*** cURL equivalent *** 
    curl -H "Accept: application/json" https://et.water.ca.gov/api/data?appKey=APPKEY&targets=75&startDate=2019-05-30&endDate=2010-05-30&dataItems=day-asce-eto,hly-asce-eto

"""
target = '75'
def cimis(current_hr):
    # Requests data from today
    today = datetime.today().strftime('%Y-%m-%d')

    headers = {
        'Accept': 'application/json',
    }

    params = (
        ('appKey', config.cimis_key),
        ('targets', '75'),
        ('startDate', today),
        ('endDate', today), 
        ('dataItems','day-asce-eto,hly-asce-eto,hly-rel-hum,hly-air-tmp')
    )

    response = requests.get('https://et.water.ca.gov/api/data', headers=headers, params=params)
    print(response.status_code)
    if (response.status_code!=200):
        return None
    data = response.json() # JSON format: https://et.water.ca.gov/Rest/Index

    records = data["Data"]["Providers"][0]["Records"][1:] # skip first line, which is NoneType

    for record in records:
        eto = record.get("HlyAsceEto")
        humidity = record.get("HlyRelHum")
        temperature = record.get("HlyAirTmp")
        if (eto.get("Value") != None):
            if (int(record.get("Hour"))==current_hr):    
                print("[%d] Et0: %.2f; Temp: %.2f Humidity: %.2f" % (int(record.get("Hour")), float(eto.get("Value")), float(temperature.get("Value")), float(humidity.get("Value"))))
                return (int(record.get("Hour")), float(eto.get("Value")), float(temperature.get("Value")), float(humidity.get("Value")))

        else:
            return None



if __name__ == '__main__':
   
    current_hour=datetime.now().time().hour
    current_hour = (current_hour)*100
    if (cimis(current_hour)!=None):
        hr, eto, temp, hum = cimis(current_hour)
    else:
        #hour that wasn't recorded
        current_hour = current_hour
