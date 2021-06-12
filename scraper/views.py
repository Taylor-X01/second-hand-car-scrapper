from django.shortcuts import render
from .models import car_data
from .scrap_selenium import run_scraper
from .form import Fields
import os
import json
from django.forms.models import model_to_dict
THIS_FILE = os.path.dirname(__file__)

context_search = {
    "mark": "dacia",
    "model": "logan",
    "city": "rabat",
    "year": "2009",
}

# Create your views here.
def get_item(request):
    forms = request.POST
    print(forms.dict())
    context_search = forms.dict()
    [data, data1] = run_scraper(context_search)
    # qs = car_data.objects.filter() 
    path = os.path.join(THIS_FILE, 'data')
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, "search_result.json")
    filepath1 = os.path.join(path, "search_result1.json")
    print("PATH:", filepath)

    with open(filepath, "r") as json_file:
        json_str = json_file.read()
        print(json_str)
        data = json.loads(json_str)
        print(data["Modele"])
    
    with open(filepath1, "r") as json_file:
        json_str = json_file.read()
        print(json_str)
        data = json.loads(json_str)
        print(data["Modele"])
   
    context = {
        'car_list_len'  : len(data["Modele"]),
        'car_model' : data["Modele"],
        'car_year'  : data["Annee"],
        'car_km'    : data["Kilometrage"],
        # 'car_city'  : data["Ville"],
        'car_price' : data["Prix"]
    }
    return render(request,'results.html',context)
