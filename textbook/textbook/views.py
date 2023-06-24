from django.shortcuts import render, HttpResponse
from textbook.generate_textbook import generate_textbook_from_user_input

def heythere(request):
    return render(request, 'kevins_demo.html')
    return HttpResponse("Hey there!")


def homepage(request):
    return render(request, 'homepage.html')

# GET Request to this URL, returns some HTML.
# The HTML contains a form
def form_for_your_own_new_textbook(request):
    return render(request, 'generate_textbook_user_input_form.html')

# HTTP POST request. Containing the user input
# This function is going to send a bunch of requests to Chat GPT
# This function is going to store chat GPT's responses in the database
def handle_form_submission(request):
    user_input_str = request.POST.get('user_input')
    context = {
        'user_input_str': user_input_str,
    }

    textbook_from_user_input = generate_textbook_from_user_input(user_input_str)
    context['book'] = textbook_from_user_input

    return render(request, 'book.html', context)

# GET request. Given a textbook id number, show the contents of that textbook
def show_single_textbook(request):
    return

# Ask the database for all of the textbooks that anyone has generated so far
# List the titles of each textbook
# Each textbook title should link to that textboook's single textbook page
def show_textbook_list(request):
    context = {}
    return render(request, 'book_list.html', context)
