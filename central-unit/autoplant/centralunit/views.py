from django.shortcuts import render
from django.http import JsonResponse
from .models import Measurement


def index(request):
    return render(request=request, template_name="centralunit/index.html")


def temperature(request):
    if request.method == 'GET':
        measurements = Measurement.objects.filter(type='temperature')
        mesurements_list = [{'time': str(m.date), 'value': m.value} for m in measurements]
        return JsonResponse(mesurements_list, safe=False)
