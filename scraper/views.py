from django.shortcuts import render
from .models import car_data

# Create your views here.
def get_item(request):
    qs = car_data.objects.filter()    
    context = {
        'car_list'  : qs,
        # 'car_brand' : qs.brand,
        # 'car_model' : qs.model,
        # 'car_year'  : qs.year,
        # 'car_km'    : qs.km,
        # 'car_city'  : qs.city,
        # 'car_price' : qs.price
    }
    return render(request,'results.html',context)