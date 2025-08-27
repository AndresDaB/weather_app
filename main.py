from dotenv import load_dotenv
import schedule
import smtplib
import requests
import time

load_dotenv()

def weatherreminder():
    city = input('Enter the city: ') 
    api_key = "YOUR API KEY FROM OPENWEATHER" 

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=es"
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Error at obtaining the weather:", response.text)
        return
    
    data = response.json()

    try:
        temperature = data["main"]["temp"]
        sky = data["weather"][0]["description"].lower()  
    except KeyError:
        print("Error in format:", data)
        return

    
    umbrella_conditions = ["rain", "storm", "cloudy"]
    need_umbrella = any(cond in sky for cond in umbrella_conditions)

    subject = "Weather reminder"
    if need_umbrella:
        body = f"Today in {city} the sky will be '{sky}' with temperatures of {temperature}°C. ¡Don't forget your umbrella!"
    else:
        body = f"Today in {city} the sky will be '{sky}' with temperatures of {temperature}°C. you will not need an umbrella"

    msg = f"Subject: {subject}\n\n{body}\n\nGretings".encode("utf-8")

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp_object:
            smtp_object.starttls()
            smtp_object.login("YOUR EMAIL", "YOUR PASSWORD")  
            smtp_object.sendmail("YOUR EMAIL", "YOUR EMAIL", msg)
        print("Email send sucessfully")
    except Exception as e:
        print("Error sending email:", e)

schedule.every().day.at("21:00").do(weatherreminder)

print("Waiting for the scheduled time...")
while True:
    schedule.run_pending()
    time.sleep(30)  # espera de 30s para no saturar CPU
