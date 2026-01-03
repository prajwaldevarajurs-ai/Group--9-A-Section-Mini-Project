import requests
from django.shortcuts import render
from .models import SearchHistory

API_KEY = "43a444546eada99fb35b41b06e7c6b11"


def home(request):
    weather_data = None
    forecast_data = []
    city_name = None
    error = None

    if request.method == "POST":
        city = request.POST.get("city")
        city_name = city

        # ---------- CURRENT WEATHER ----------
        weather_url = (
            f"https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={API_KEY}&units=metric"
        )
        weather_response = requests.get(weather_url)
        weather_json = weather_response.json()

        # ❌ Invalid city or API error
        if weather_json.get("cod") != 200:
            error = "City not found. Please enter a valid city name."
        else:
            weather_data = weather_json

            # ✅ Save valid city to search history
            SearchHistory.objects.create(city=city)

            # ---------- 5-DAY FORECAST ----------
            forecast_url = (
                f"https://api.openweathermap.org/data/2.5/forecast"
                f"?q={city}&appid={API_KEY}&units=metric"
            )
            forecast_response = requests.get(forecast_url)
            forecast_json = forecast_response.json()

            # Extract ONE forecast per day (12:00 PM)
            if forecast_json.get("cod") == "200":
                for item in forecast_json.get("list", []):
                    if "12:00:00" in item.get("dt_txt", ""):
                        forecast_data.append({
                            "date": item["dt_txt"],
                            "temp": item["main"]["temp"],
                            "humidity": item["main"]["humidity"],
                            "wind": item["wind"]["speed"],
                        })

    return render(
        request,
        "home.html",
        {
            "weather": weather_data,
            "forecast": forecast_data,
            "city": city_name,
            "error": error,
        }
    )
    
def searchhistory(request):
    searches = SearchHistory.objects.all().order_by("-searched_at")
    return render(request, "searchhistory.html", {"searches": searches})

def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")



