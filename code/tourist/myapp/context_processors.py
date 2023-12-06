from datetime import datetime
from myapp.models import *
import json
from .views.weather import get_weather_data

def get_all_attractions(request):
    attractions_search = list(Attractions.objects.filter(ispet=False).values_list("a_name", flat=True))
    attractions_search_json = json.dumps(attractions_search)
    return {"attractions_search_json":attractions_search_json}


def get_now_weather(request):
    current_datetime = datetime.now()

    current_year = current_datetime.year
    current_month = current_datetime.month
    current_day = current_datetime.day
    current_hour = current_datetime.hour
    current_minute = current_datetime.minute
    text = get_weather_data("中正區",current_year,f'{current_month:02d}',f'{current_day:02d}',f'{int(current_hour*60+current_minute)}')
    if "降雨機率" in text :
        s = text.split("%")
        rain = int(s[0][4:])
        if rain > 50:
            get_now_weather_json = json.dumps({"get_now_weather_json":"rain"})
        else:
            get_now_weather_json = json.dumps({"get_now_weather_json":"sun"})
        
    return {"get_now_weather_json":get_now_weather_json}