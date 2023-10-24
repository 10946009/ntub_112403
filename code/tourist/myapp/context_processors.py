from myapp.models import *
import json

def get_all_attractions(request):
    attractions_search = list(Attractions.objects.values_list("a_name", flat=True))
    attractions_search_json = json.dumps(attractions_search)
    return {"attractions_search_json":attractions_search_json}