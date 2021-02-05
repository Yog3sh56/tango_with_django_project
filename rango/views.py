from django.shortcuts import render
from django.http import HttpResponse
# Import the Category model
from rango.models import Category
from rango.models import Page


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
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    # Render the response and send it back
    return render(request, 'rango/index.html', context=context_dict)


# View from the exercise
def about(request):
    # return HttpResponse("Rango says here is the about page.<a href='/rango/'>Index</a>")
    return render(request, 'rango/about.html')


# View for categories
def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass to the template rendering engine
    context_dict = {}

    try:
        # can we find a category name slug with the given name?
        category = Category.objects.get(slug=category_name_slug)

        # Retrieve all associated pages
        pages = Page.objects.filter(category=category)

        # Adds our results list to the template context under name pages
        context_dict['pages'] = pages

        # We also need to add the category object from the database to the context dictionary
        context_dict['category'] = category

    except Category.DoesNotExist:
        # We get here if the category is not found. Dont really need to do anything here
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)
