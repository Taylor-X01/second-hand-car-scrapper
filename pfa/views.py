from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

# def home_page(request):
#     my_title = "Hello, Welcome to the Page !!"
#     return render(request, 'hello_world.html', {"title":my_title})


# def contact_page(request):
#     my_title = "Hello, Welcome to the Contact page !!"
#     return render(request, 'contact.html', {"title": my_title})


# def about_page(request):
#     my_title = "Hello, Welcome to the About Page !!"
#     return render(request, 'about.html', {"title": my_title})

# def example_page(request):
#     my_title        = "This is an example to render a txt file"
#     context         = {"title":my_title}
#     template_name   = "example.txt"  
#     template_obj    = get_template(template_name)
#     rendered_item   = template_obj.render(context)

#     return render(request,'hello_world.html',{"title":rendered_item})

def main_page(request):
    return render(request,'home.html')

## RESULT PAGE

def result_page(request):
    mark = "Marque"
    model = "Modèle"
    price = "prixxxx"
    city = "Rabat"

    context = {
        'item_name':mark,
        'item_model':model,
        'item_price':price,
        'item_city':city
    }

    return render(request,'results.html',context)