from django.shortcuts import render
from csvs.models import carPost
from .scrap_selenium import run_scraper
import os
import csv
from pathlib import Path

THIS_FILE = os.path.dirname(__file__)
BASE_DIR = Path(__file__).resolve().parent.parent


# context_search = {
#     "mark": "dacia",
#     "model": "duster",
#     "city": "rabat",
#     "year": "2009",
# }

# Create your views here.
def get_item(request):
    carPost.objects.all().delete()
    forms = request.POST
    print(forms.dict())
    context_search = forms.dict()
    run_scraper(context_search)
    
    path = os.path.join(BASE_DIR, 'scraper', 'data')
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, "search_result_wandaloo.csv")
    filepath1 = os.path.join(path, "search_result_moteur.csv")

    with open(filepath, "r") as csv_file:
        csv_str = csv.reader(csv_file)

        for i, row in enumerate(csv_str):
            if i == 0:
                pass
            else:
                print(row)
                carPost.objects.create(
                    url=row[0],
                    model=row[1],
                    option=row[2],
                    price=row[3],
                    vendor=row[4],
                    year=row[5],
                    city=row[6],
                    main=row[7],
                    km=row[8],
                    carb=row[9],
                    trans=row[10],
                    img = row[11],
                )

    with open(filepath1, "r") as csv_file:
        csv_str = csv.reader(csv_file)

        for i, row in enumerate(csv_str):
            if i == 0:
                pass
            else:
                print(row)
                carPost.objects.create(
                    url=row[0],
                    model=row[1],
                    option=row[2],
                    price=row[3],
                    vendor=row[4],
                    year=row[7],
                    city=row[5],
                    main=row[10],
                    km=row[6],
                    carb=row[9],
                    trans=row[8],
                    img=row[11]
                )
    
    context = {
        'car_list'  : carPost.objects.get_queryset,
        'result_num': carPost.objects.all().count(),
    }
    return render(request,'results.html',context)
