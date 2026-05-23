from django.shortcuts import render
import random
import time
# Create your views here.

def main(request):
    '''Show the main page.'''
 
 
    template_name = "restaurant/main.html"
    return render(request, template_name)

def order(request):
    '''Show the web page with the form.'''
    menu_items = [("Chop Suey", 6.29), ("Sushi", 13.99), ("Pastrami", 8.50)]
    specials = [("Concrete Block", 1.50), ("Wood Block", 2.50), ("Wheelchair (not in use)", 47.50)]
    toppings = [("Pepperoni", 1.50), ("Mushrooms", 0.50), ("Sausage", 1.50)]
    pizza = ("Pizza", 14.99)
    context = {
        'items': menu_items,
        'special': random.choice(specials),
        'toppings': toppings,
        'pizza': pizza
    }
 
 
    template_name = "restaurant/order.html"
    return render(request, template_name, context)

def confirmation(request):
    '''Process the form submission, and generate a result.'''
 
 
    template_name = "restaurant/confirmation.html"
    name = request.POST['name']
    phone = request.POST['phone']
    email = request.POST['email']
    special_instructions = request.POST['special_instructions']
 
 
    # read the form data into python variables:
    if request.POST:
        ordered = request.POST.getlist('checklist')
        time_plus_wait = time.time() + (random.randint(30, 60) * 60)
        price = 0
        items = []
        split_list = [item.split(',') for item in ordered] 
        for i in split_list:
            items += i[0]
            price += float(i[1])


        

        context = {
            'cost': round(price, 2),
            'full_cost': round((price * 1.07), 2),
            'special_instructions': special_instructions,
            'email': email,
            'phone': phone,
            'name': name,
            'items': split_list,
            'time': time.ctime(time_plus_wait),
        }
 
 
    return render(request, template_name, context=context)

