import requests
from datetime import datetime
import smtplib
import time

TO_ADDRESS = "victornwaonicha@gmail.com"
MY_EMAIL = "youngvivianchinyere@gmail.com"
MY_PASSWORD = "brwr xsno kezk tkpi"

MY_LAT = 6.524379
MY_LNG = 3.379206

# If the ISS is close to my current position.
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    is_latitude = float(data["is_position"]["latitude"])
    is_longitude = float(data["is_longitude"]["longitude"])

    if MY_LAT-5 <= is_latitude <= MY_LAT+5 and MY_LNG-5 <= is_longitude <= MY_LNG+5:
        return True

# And it is currently dark time.
def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LNG,
        "formatted": 0
    }
    response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()

    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True

# Send me an email to tell me to look up
while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()  # secure the connection
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=TO_ADDRESS,
                msg="Subject:Look up!\n\nThe ISS is above you in the sky."
            )


