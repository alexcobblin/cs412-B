from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random
 
 
import time
 
def home_page(request):
    '''Define a view to show the 'home.html' template.'''
 
 
    # the template to which we will delegate the work
    template = 'quotes/home.html'
 
 
    # a dict of key/value pairs, to be available for use in template
    context = {
        'current_time': time.ctime(),
        'letter1' : chr(random.randint(65,90)),
        'letter2' : chr(random.randint(65,90)),
        'number' : random.randint(1,10),
    }
 
 
    return render(request, template, context)

def about(request):
    '''Define a view to show the 'about.html' template.'''
 
 
    # the template to which we will delegate the work
    template = 'quotes/about.html'
 
 
    # a dict of key/value pairs, to be available for use in template
    context = {
        'current_time': time.ctime(),
    }
 
 
    return render(request, template, context)
def quote(request):
    '''Define a view to show the 'quote.html' template.'''
 
 
    # the template to which we will delegate the work
    template = 'quotes/quote.html'
    quotes = ["C is for cookie that's good enough for me.", "Om Nom Nom Nom",
              "Home is where heart is. Heart where cookie is. Math clear: home is cookie.",
              "Sometimes me think, what is friend? And then me say: a friend is someone to share last cookie with.",
              "I'd give you a cookie, but I ate it.", "Me Love to Eat Cookies. Sometimes eat whole, sometimes me chew it.",
              "Keep Calm & Eat Cookies"]
    images = [
        "https://i.scdn.co/image/ab6761610000e5eba3a7cba23d68a4e73c3b8155", "https://www.middlebury.edu/sites/default/files/2019-08/cookie-monster-portrait.jpg?fv=dkM5B0Io",
        "https://cdn.britannica.com/66/218266-050-77C3D624/Cookie-Monster-Sesame-Street-2016.jpg",
        "https://www.thetakeout.com/images/98ccfa6d03b97c79bafee62c57d8e47e.jpg"
    ]
 
 
    # a dict of key/value pairs, to be available for use in template
    context = {
        'current_time': time.ctime(),
        'cookie': random.choice(quotes),
        'monster': random.choice(images),
    }
 
 
    return render(request, template, context)
def show_all(request):
    '''Define a view to show the 'quote.html' template.'''
 
 
    # the template to which we will delegate the work
    template = 'quotes/show_all.html'
    quotes = ["C is for cookie that's good enough for me.", "Om Nom Nom Nom",
              "Home is where heart is. Heart where cookie is. Math clear: home is cookie.",
              "Sometimes me think, what is friend? And then me say: a friend is someone to share last cookie with.",
              "I'd give you a cookie, but I ate it.", "Me Love to Eat Cookies. Sometimes eat whole, sometimes me chew it.",
              "Keep Calm & Eat Cookies"]
    images = [
        "https://i.scdn.co/image/ab6761610000e5eba3a7cba23d68a4e73c3b8155", "https://www.middlebury.edu/sites/default/files/2019-08/cookie-monster-portrait.jpg?fv=dkM5B0Io",
        "https://cdn.britannica.com/66/218266-050-77C3D624/Cookie-Monster-Sesame-Street-2016.jpg",
        "https://www.thetakeout.com/images/98ccfa6d03b97c79bafee62c57d8e47e.jpg"
    ]
 
 
    # a dict of key/value pairs, to be available for use in template
    context = {
        'current_time': time.ctime(),
        'cookies': quotes,
        'images' : images,
    }
 
 
    return render(request, template, context)