from django.shortcuts import render
from django.http import HttpResponse
# Import the Category model
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect


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


def add_category(request):
    form = CategoryForm()

    # A HTTP POST? POST => did the user submit data via the form?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this. for now just redirect user back to index view
            return redirect('/rango/')
        else:
            # Just print them to the terminal
            print(form.errors)

    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'forms': form})



