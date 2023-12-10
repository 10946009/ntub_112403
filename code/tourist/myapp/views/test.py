from django.shortcuts import render
from datetime import datetime

import googlemaps
from myapp.models import *
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .viewsConst import GOOGLE_PLACES_API_KEY
from .recommend import recommend,recommend_maybe,recommend_user_favorite,recommend_pet
from .recommend_near import recommend_near
from .final_order import final_order
import requests
from geopy.geocoders import Nominatim
from django.template.loader import render_to_string  # 頁面轉成html
import os
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
import json
from .weather import get_weather_data



def test(request):
    key = GOOGLE_PLACES_API_KEY
    return render(request, "test_gps.html",locals())