from django.shortcuts import render
from django.http import HttpResponse
from insights.utils import *
import json

def home(request):
    data = get_coach_data()
    metrics = get_metrics(data)
    return render(request, 'home.html', {'metrics': metrics})
    
def api_data(request):
    data = get_coach_data()
    return HttpResponse(json.dumps(data))
    
def api_coach_data_matrix(request):
    data = get_coach_data()
    matrix = get_coach_matrix(data)
    results = {'packageNames': get_schools(),
                'matrix': matrix}
    return HttpResponse(json.dumps(results))