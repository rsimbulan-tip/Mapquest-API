from flask import Flask
from flask import request
from flask import render_template
import requests
import urllib.parse
import sys

main_api = "https://www.mapquestapi.com/directions/v2/route?" 
key = "aXced6NG8EtfGmVNZU2hZaKjCJlJH3gI"

sample = Flask(__name__)

@sample.route("/", methods=['GET','POST'])
def index():
    global orig, dest
    if request.method == "GET":
        return render_template("index.html")

    if request.method == "POST":
        orig = request.form['orig']
        dest = request.form['dest']

        url = main_api + urllib.parse.urlencode({"key": key, "from":orig, "to":dest})
        print("URL: " + (url))
        json_data = requests.get(url).json()
        json_status = json_data["info"]["statuscode"]

        if json_status == 0:
            print("API Status: " + str(json_status) + " = A successful route call.\n")
            print("=============================================")
            tripDuration = json_data["route"]["formattedTime"]
            print("Trip Duration    :" + tripDuration)
            kilometers = (json_data["route"]["distance"])*1.61
            print("Kilometers       :" + str("{:.2f}".format(kilometers)))
            fuelUsed = (json_data["route"]["fuelUsed"])*3.78
            print("Fuel Used (Ltr)  :" + str("{:.2f}".format(fuelUsed)))
            print("=============================================")
            for each in json_data["route"]["legs"][0]["maneuvers"]:
                print((each["narrative"]) + " (" + str("{:.2f}".format((each["distance"])*1.61) + " km)"))
            print("=============================================")
            print("Additional Information")
            tollRoad = json_data["route"]["hasTollRoad"]                #inform users if there are toll fees ahead
            if tollRoad == 0:
                toll="None"
                print("Toll Road        :" + toll)
            else:
                toll="Yes"
                print("Toll Road        :" + toll)
            seasonalClosure = json_data["route"]["hasSeasonalClosure"]  #inform users if there are seasonal closures ahead
            if seasonalClosure == 0:
                seasonal="None"
                print("Seasonal Clsoure :" + seasonal)
            else:
                seasonal="Yes"
                print("Seasonal Closure :" + seasonal)
            countryCross = json_data["route"]["hasCountryCross"]        #inform users if they will be crossing another country to prepare for border inspections
            if countryCross == 0:
                country="None"
                print("Cross Country    :" + country)
            else:
                country="Yes"
                print("Cross Country    :" + country)
            latitude = json_data["route"]["boundingBox"]["lr"]["lat"]
            print("Dest Latitude    :" + str(latitude))    #for a more accurate waze navigation
            longitude = json_data["route"]["boundingBox"]["lr"]["lng"]
            print("Dest Longitude   :" + str(longitude))    #for a more accurate waze navigation
            print("=============================================\n")
        
        elif json_status == 402:
            print("******************************************")
            print("Status Code: " + str(json_status) + "; Invalid user inputs for one or both locations.")
            print("**********************************************\n")
        elif json_status == 611:
            print("******************************************")
            print("Status Code: " + str(json_status) + "; Missing an entry for one or both locations.")
            print("**********************************************\n")
        else:
            print("********************************************************************")
            print("For Staus Code: " + str(json_status) + "; Refer to:")
            print("https://developer.mapquest.com/documentation/directions-api/status-codes")
            print("************************************************************************\n")
    return render_template('index.html', orig=orig, dest=dest, tripDuration=tripDuration, 
    kilometers=kilometers, fuelUsed=fuelUsed, toll=toll, seasonal=seasonal, country=country,
    latitude=latitude, longitude=longitude)

if __name__=="__main__":
    sample.run(host="0.0.0.0", port=8080)