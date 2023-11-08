from django.shortcuts import render, redirect
from myapp.models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string

def get_attractions_data(request):
    data = None
    if  request.GET.get('aidlist') :
        aidlist = request.GET.get('aidlist')
        print('aidlist',aidlist)
        aidlist = map(int,aidlist.split(','))
        data = Attractions.objects.filter(id__in=aidlist)

    return render(request, 'create_bottom.html', {'data': data})