from datetime import datetime
import config
import requests

"""
*** cURL equivalent *** 
    curl -H "Accept: application/json" https://et.water.ca.gov/api/data?appKey=APPKEY&targets=75&startDate=2019-05-30&endDate=2010-05-30&dataItems=day-asce-eto,hly-asce-eto

"""
def cimis():
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
    data = response.json() # JSON format: https://et.water.ca.gov/Rest/Index
    records = data["Data"]["Providers"][0]["Records"][1:] # skip first line, which is NoneType
    #print(records)

    for record in records:
        eto = record.get("HlyAsceEto")
        humidity = record.get("HlyRelHum")
        temperature = record.get("HlyAirTmp")
        #print(humidity)
        # prints only available data
        if (eto.get("Value") != None):
            print("[%d] Et0: %.2f; Humidity: %.2f" % (int(record.get("Hour")), float(eto.get("Value")), float(humidity.get("Value"))))

            return (int(record.get("Hour")), float(eto.get("Value")), float(temperature.get("Value")), float(humidity.get("Value")))
