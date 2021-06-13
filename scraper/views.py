from django.shortcuts import render
from .models import car_data
from .scrap_selenium import run_scraper
from .form import Fields
import os
import csv
from django.forms.models import model_to_dict
THIS_FILE = os.path.dirname(__file__)

# context_search = {
#     "mark": "dacia",
#     "model": "duster",
#     "city": "rabat",
#     "year": "2009",
# }

# Create your views here.
def get_item(request):
    forms = request.POST
    print(forms.dict())
    context_search = forms.dict()
    [data, data1] = run_scraper(context_search)
    
    path = os.path.join(THIS_FILE, 'data')
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, "search_result_wandaloo.csv")
    filepath1 = os.path.join(path, "search_result_moteur.csv")
    print("PATH:", filepath)

    with open(filepath, "r") as csv_file:
        csv_str = csv.reader(csv_file)
        print(csv_str)
        data_wandaloo = list(csv_str)
        print("------> Wandaloo <-------\n",data_wandaloo)
    
    with open(filepath1, "r") as csv_file:
        csv_str = csv.reader(csv_file)
        print(csv_str)
        data_moteur = list(csv_str)
        print("------> Moteur <------:\n",data_moteur)
   
    context = {
        'car_list_len'  : len(data),
        'car_model' : data["Modele"],
        'car_year'  : data["Annee"],
        'car_km'    : data["Kilometrage"],
        'car_city'  : data["Ville"],
        'car_price' : data["Prix"]
    }
    return render(request,'results.html',context)
