from bson import ObjectId
from django.shortcuts import redirect, render, HttpResponse
from pymongo import MongoClient
from textbook.generate_textbook import generate_textbook_from_user_input, get_body_contents_from_html_file

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
    user_input_str = request.POST.get('user_input', '')

    textbook_from_user_input = generate_textbook_from_user_input(user_input_str)
    new_book_id = textbook_from_user_input.get('book_id')
    print(f"Created a new Book with ID: {new_book_id}")
    return redirect(f'/book?id={new_book_id}')


def given_a_id_return_a_book_with_that_id():
    return


# GET request. Given a textbook id number, show the contents of that textbook
def show_single_textbook(request):
    book_id_requested_by_user = request.GET.get('id')
    print(book_id_requested_by_user)

    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING)
    db = client['textbook']
    books_collection = db['books']

    # my_id_str = "64977324c335fdd18efa2d7f"
    my_id_str = book_id_requested_by_user

    objInstance = ObjectId(my_id_str)
    my_book = books_collection.find_one({"_id": objInstance})

    chapters_reformatted = []
    for chapter in my_book.get('chapters', []):
        content_reformatted = get_body_contents_from_html_file(chapter.get('chapter_content', ''))
        discussion_questions_reformatted = get_body_contents_from_html_file(chapter.get('subtopic_discussion_questions', ''))
        test_prep_questions_reformatted = get_body_contents_from_html_file(chapter.get('test_prep_questions', ''))
        resources_reformatted = get_body_contents_from_html_file(chapter.get('resources', ''))
        reformatted_chapter = {
            **chapter,
            'chapter_content': content_reformatted,
            'discussion_questions_reformatted': discussion_questions_reformatted,
            'test_prep_questions_reformatted': test_prep_questions_reformatted,
            'resources_reformatted': resources_reformatted,
        }
        chapters_reformatted.append(reformatted_chapter)


    context = {
        'book': {
            'title': my_book.get('title'),
            'chapters': chapters_reformatted,
        }
    }
    return render(request, 'book.html', context)

# Ask the database for all of the textbooks that anyone has generated so far
# List the titles of each textbook
# Each textbook title should link to that textboook's single textbook page
def show_textbook_list(request):

    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING)
    db = client['textbook']
    books_collection = db['books']

    all_books_in_db = books_collection.find()

    context = {
        'all_books': all_books_in_db,
    }

    return render(request, 'book_list.html', context)
