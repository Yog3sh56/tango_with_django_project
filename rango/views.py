from django.shortcuts import render
from django.http import HttpResponse
# Import the Category model
from rango.models import Category


# Create your views here.
def index(request):
    # Construct a dictionary to pass to the template engines as its context.
    # Note the key boldmessage matches to {{ boldmessage }} in the template!
    # context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}

    # Return a rendered response to send to the client (instead of an HttpResponse
    # We make use fo teh shortcut function to make out lives easier.
    # note that the first parameter is teh template we wish to use
    # return render(request, 'rango/index.html', context=context_dict)

    # Query teh database for a list of all categories currently stored, order them by the number of likes in descending
    # order. Retrieve the top 5 only and place the list in our context_dict  (with the bold message) that will be
    # passed to the template.

    category_list = Category.objects.order_by('-likes')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list

    # Render the response and send it back
    return render(request, 'rango/index.html', context=context_dict)


# View from the exercise
def about(request):
    # return HttpResponse("Rango says here is the about page.<a href='/rango/'>Index</a>")
    return render(request, 'rango/about.html')
