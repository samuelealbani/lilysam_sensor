import machine
from machine import Timer
import urequests as requests
import network
import time

timer = Timer()

counter=0


# Wifi Credentials
SSID = "EE-Hub-3mLD"
PSK = "Liakos10Liakos10"


def connect_to_wifi(ssid, psk):
    # Enable Wifi in Client Mode
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    # Connect to Wifi, keep trying until failure or success
    wlan.connect(ssid, psk)

    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to Connect")
        time.sleep(5)
    if not wlan.isconnected():
        raise Exception("Wifi not available")
    print("Connected to WiFi")

def addTest(timer):
    global counter
    url = "https://eu-west-2.aws.data.mongodb-api.com/app/data-mxvxa/endpoint/data/v1/action/insertOne"
    headers = { "api-key": "LVrqps10Se46eEZjOmT20mGYLQaOPyLviQ3fnhGxZU4zqD4WEBsakffxHWn4M8W9" }

    documentToAdd = {"device": "MyPico", "readings": counter}

    insertPayload = {
        "dataSource": "SensorsCluster0",
        "database": "myDatabase",
        "collection": "recipes",
        "document": documentToAdd,
    }

    print("sending...")

    response = requests.post(url, headers=headers, json=insertPayload)

    print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))

    if response.status_code == 201:
        print("Added Successfully")
    else:
        print("Error")

    # Always close response objects so we don't leak memory
    response.close()
    counter=counter+1

try:
    connect_to_wifi(SSID, PSK)
    
    timer.init(freq=2, mode=Timer.PERIODIC, callback=addTest)


except Exception as e:
    print(e)

# Stop the Wifi
# try:
#     wlan.active(False)
# except Exception as e:
#     print(e)