from django.shortcuts import render
from .models import carPost
from scraper.scrap_selenium import run_scraper
import os
import csv
from pathlib import Path

THIS_FILE = os.path.dirname(__file__)
BASE_DIR = Path(__file__).resolve().parent.parent
# Create your views here.


def get_data(request):
    forms = request.POST
    print(forms.dict())
    context_search = forms.dict()
    [data, data1] = run_scraper(context_search)

    path = os.path.join(BASE_DIR, 'scraper','data')
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, "search_result_wandaloo.csv")
    filepath1 = os.path.join(path, "search_result_moteur.csv")

    with open(filepath, "r") as csv_file:
        csv_str = csv.reader(csv_file)

        for i,row in enumerate(csv_str):
            if i==0:pass
            else:
                print(row)
                carPost.objects.create(
                    model   =   row[0],
                    option  =   row[1],
                    price   =   row[2],
                    vendor  =   row[3],
                    tel     =   row[4],
                    year    =   row[5],
                    city    =   row[6],
                    main    =   row[8],
                    km      =   row[9],
                    carb    =   row[10],
                    trans   =   row[11],
                )

    with open(filepath1, "r") as csv_file:
        csv_str = csv.reader(csv_file)

        for i, row in enumerate(csv_str):
            if i==0:pass
            else:
                print(row)
                carPost.objects.create(
                    model   =   row[0],
                    price   =   int(row[1]),
                    vendor  =   row[2],
                    year    =   row[5],
                    city    =   "-",
                    main    =   row[8],
                    km      =   int(row[4]),
                    carb    =   row[7],
                    trans   =   row[6],
                )

                
    return
