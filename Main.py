import urllib.request
import os
import json
import calendar
from datetime import date
from datetime import datetime

API_KEY = os.environ.get('OPEN_WEATHER_API_KEY') # Request API key from enviroment variables
LOCATION = 3451328 # Ribeirão Preto city ID
HUMIDITY = 70 # Humidity threshold for bringing an umbrella 

days = [0,0,0,0,0]
umbrella = [False, False, False, False, False]
rainyDays = ["", "", "", "", ""]

mainText = "You should take an umbrella in these days: "
notRaining = "Luckly you will not have to take an umbrella with you for the next 5 days!"

# defining global variables timestamp for the next 5 days
def next_days():
    global days

    today = date.today()
    midnight = datetime.combine(today, datetime.min.time())
    midnightTs = midnight.timestamp()
    for i in range(len(days)):
        days[i] = midnightTs + (86400*(i+1))

# convert weekday ID to full length string
def weekDayName(ts):
    dt_object = datetime.fromtimestamp(ts)
    dayIndex = dt_object.weekday()
    return calendar.day_name[dayIndex]

# count how many of the next 5 days will be rainig
def countRainyDays():
    count = 0
    for i in range(len(umbrella)):
        if umbrella[i]:        
            rainyDays[count] = weekDayName(days[i])
            count += 1
    return count


# defining the umbrella requirement for each day
def request_umbrella(dt):
    for i in range(len(days)):
        if (dt>days[4-i]):
            umbrella[4-i] = True
            break

# constructs the output text based on the number of rainy days
def textConstructor(count):
    finalText = ""
    if (count == 0):
        finalText = notRaining
    elif (count == 1):
        finalText += mainText
        finalText += rainyDays[0]
    else:
        finalText += mainText
        for i in range(count):
            if (i!=0 and i!=(count-1)):
                finalText += ", "
            if (i==(count-1)):
                finalText += " and "
            finalText += rainyDays[i]

    return finalText


# Use json module to load the data
def get_future_weather(location, api_key):
    url = "https://api.openweathermap.org/data/2.5/forecast?id={}&units=metric&appid={}".format(location, api_key)
    weatherUrl = urllib.request.urlopen(url)
    if (weatherUrl.getcode() == 200):
        data = weatherUrl.read()
        return json.loads(data)
    else:
        print("Received error, cannot parse results")
        return False


def main():

    next_days()

    forecast = get_future_weather(LOCATION, API_KEY)

    if (forecast != False):
        for i in forecast["list"]:
            if(i["main"]["humidity"] > HUMIDITY):
                dt = i["dt"]
                request_umbrella(dt)
        finalText = textConstructor(countRainyDays())
        print (finalText)
        

if __name__ == '__main__':
    main()