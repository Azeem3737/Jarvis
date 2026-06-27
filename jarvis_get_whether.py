import os
import requests
import logging
from dotenv import load_dotenv
from livekit.agents import function_tool  # ✅ Correct decorator

load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def detect_city_by_ip() -> str:
    try:
        logger.info("IP کے ساحل شہر detect کرनے کی کوشش کی جا رہی ہے")
        ip_info = requests.get("https://ipapi.co/json/").json()
        city = ip_info.get("city")
        if city:
            logger.info(f"IP سے شہر Detect کیا گیا: {city}")
            return city
        else:
            logger.warning("City detect کرنے میں ویفیل, default 'Islamabad' استعمال کیا جا رہا ہے۔")
            return "Islamabad"
    except Exception as e:
        logger.error(f"IP سے city detect کرنے میں error آیا: {e}")
        return "Islamabad"

@function_tool
async def get_weather(city: str = "") -> str:
    
    api_key = os.getenv("OPENWEATHER_API_KEY")

    if not api_key:
        logger.error("OpenWeather API key missing ہے")
        return "Environment variables میں OpenWeather API key نہیں ملی۔"

    if not city:
        city = detect_city_by_ip()

    logger.info(f"City کے لیے weather fetch کیا جا رہا ہے۔: {city}")
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            logger.error(f"OpenWeather API میں error آیا۔: {response.status_code} - {response.text}")
            return f"Error: {city} کے لیے weather fetch نہیں ملا۔ مہربانی کر کے city name چیک کریں۔"

        data = response.json()
        weather = data["weather"][0]["description"].title()
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        result = (f"Weather in {city}:\n"
                  f"- Condition: {weather}\n"
                  f"- Temperature: {temperature}°C\n"
                  f"- Humidity: {humidity}%\n"
                  f"- Wind Speed: {wind_speed} m/s")

        logger.info(f"Weather result: \n{result}")
        return result

    except Exception as e:
        logger.exception(f"Weather fetch وقت exception آیا: {e}")
        return "Weather fetch وقت ایک error آیا"
    
