import requests
from geopy.geocoders import Nominatim
import subprocess
import importlib

def get_user_location(api_key):
    url = "http://ip-api.com/json"
    response = requests.get(url)
    if response.status_code == 200:
        location_data = response.json()
        city = location_data.get("city", "")
        lat = location_data.get("lat", None)
        lon = location_data.get("lon", None)
        return lat, lon, city
    else:
        print("Konum bilgisi alınamadı.")
        return None, None, None

def get_weather_data(api_key, lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Hava durumu verileri alınamadı.")
        return None

def calculate_soil_moisture(temperature, humidity):
    return (humidity / 100) * (100 - temperature) # Yüzde cinsinden topraktaki nem oranı

def install_required_packages():
    required_packages = ["geopy", "requests"]  # Diğer kullanılan kütüphaneleri buraya ekleyin.

    for package in required_packages:
        try:
            importlib.import_module(package)
        except ImportError:
            try:
                subprocess.run(["pip", "install", package], check=True)
            except subprocess.CalledProcessError:
                print(f"{package} kütüphanesi yüklenirken bir hata oluştu. Lütfen manuel olarak yükleyin.")
                return False
    return True

def main():
    api_key = "d8fe572b09193829e2b9b7494231f7aa"

    # Gereksinimleri yükle
    if not install_required_packages():
        return

    lat, lon, city = get_user_location(api_key)

    if lat is not None and lon is not None:
        weather_data = get_weather_data(api_key, lat, lon)
        if weather_data:
            temperature = weather_data["main"]["temp"]
            humidity = weather_data["main"]["humidity"]

            soil_moisture = calculate_soil_moisture(temperature, humidity)

            print(f"Bulunduğunuz şehir: {city}")
            print(f"Aktüel sıcaklık: {temperature} °C")
            print(f"Aktüel nem oranı: {humidity}%")
            print(f"Topraktaki nem oranı: {soil_moisture}%")

            if soil_moisture < 30:
                print("Toprak kurudur, bahçeyi sulayın.")
            else:
                print("Toprak yeterince nemli, bahçeyi sulamayın.")

if __name__ == "__main__":
    main()