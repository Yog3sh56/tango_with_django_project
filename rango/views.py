from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    # Construct a dictionary to pass to the template engines as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    # Return a rendered response to send to the client (instead of an HttpResponse
    # We make use fo teh shortcut function to make out lives easier.
    # note that the first parameter is teh template we wish to use
    return render(request, 'rango/index.html', context=context_dict)

# View from the exercise
def about(request):
    return HttpResponse("Rango says here is the about page.<a href='/rango/'>Index</a>")
