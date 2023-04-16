from django.shortcuts import render
from datetime import datetime

import googlemaps
import os
import populartimes
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
#在這定義函數

# def sayhello(request,username):
#     now = datetime.now

#     return render(request,"sayhello.html",locals())

def sayhello(request):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path, override=True)  # 設定 override 才會更新變數哦！
    GOOGLE_PLACES_API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
    print(GOOGLE_PLACES_API_KEY)

    # Client
    gmaps = googlemaps.Client(key=GOOGLE_PLACES_API_KEY)
    # geocode_result = gmaps.geocode("臺北市立動物園")
    p =populartimes.get_id(GOOGLE_PLACES_API_KEY, 'ChIJj4EySmCqQjQRZte0Cf0G_qo')
    rating = p['rating']
    rating_n=p['rating_n']
    time_spent=p['time_spent']
    print(p)
    print(time_spent)
    return render(request,"sayhello.html",locals())
