from django.shortcuts import render
from django.http import HttpResponse
# Import the Category model
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login


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


# View for add_category template
def add_category(request):
    # we have add the CategoryForm class in forms.py that was imported on the top
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
    return render(request, 'rango/add_category.html', {'form': form})


# View for add Pages allowing users to add pages to a given category
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == "POST":
        form = PageForm(request.POST)

    if form.is_valid():
        if category:
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()

            return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)


def register(request):
    # A boolean value to keep track if the registration was successful
    registered = False

    if request.method == 'POST':
        # Grab information from the form
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If both forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database
            user = user_form.save()

            # Now we need to hash the password with the set_password method
            # Once hashed we then update the user object.
            user.set_password(user.password)
            user.save()

            # Now we sort out the UserProfile
            # Since we need to set the user attribute ourselves, we set commit=Fasle. This delays saving the model
            # until we are ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now the picture time. Did user provide with a picture? If so we need to get it from the input form and
            # put int in the UserProfile model
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Thats all that we need to check, well we havent checked the personal website thing yet

            # Now save the profile instance
            profile.save()

            # Update the variable to indicate that the registration was successful
            registered = True
        else:
            print(user_form.errors, profile_form.errors)

    else:
        # If not POST request then we render the form using ModelForm instances.
        # These forms will be empty and ready for user input
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


def user_login(request):
    # If the request is a POST then extract the information from the request
    if request.method == 'POST':

        # Gather the information from login form provided by the user We use get method instead of getting it as a
        # list is because, get would return None if it doesnot exist while getting it as a list(or value of a given
        # key) would raise an KeyError
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check with django's built in machinery to attempt to check if username and password are valid
        # Returns an user object if they are valid

        user = authenticate(username=username, password=password)

        # So if we do have user object then the details are correct, if not its invalid
        if user:
            # Also check if the account is active
            if user.is_active:
                # If details are correct, we can log the user in and send them to the homepage
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f'Invalid login details: {username}, {password}')
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, 'rango/login.html')
