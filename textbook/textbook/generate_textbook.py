import openai
import os
import sys
from django.utils.safestring import mark_safe
from bson import ObjectId
from bs4 import BeautifulSoup

sys.path.append("..")
from secret_values import MY_SECRET_CHAT_GPT_KEY_PLS_DONT_STEAL_THIS_THX


openai.api_key = MY_SECRET_CHAT_GPT_KEY_PLS_DONT_STEAL_THIS_THX  # replace with your OpenAI API key

DEBUG = False
NUMBER_OF_CHAPTERS = 5
EDUCATION_LEVEL = 'simple college'
MODEL = 'gpt-3.5-turbo'
NUMBER_OF_DISCUSSION_QUESTIONS = 'five'
NUMBER_OF_ADDITIONAL_RESOURCES = 'five'
NUMBER_OF_AUTO_SUGGESTED_BOOK_IDEAS = 'five'

def get_user_input_from_command_line():
    print("Enter a topic you want to learn about. Then hit enter:")
    the_user_response = input("")
    return the_user_response


def get_user_input_plus_our_prompt(the_user_response):
    return f"{the_user_response} for {EDUCATION_LEVEL} students"

def ask_gpt_to_list_topics(raw_user_input):
    if DEBUG:
        return "1. Music\n2.Dance\n3.Singing"
    
    my_prompt = f"Imagine you are going to write a textbook about {raw_user_input}. Generate a list of ten topics related to {raw_user_input}. Return a list where each item in the list starts with a number."
    return ask_chat_gpt_and_get_response(my_prompt, my_prompt)


def divide_response_into_subtopics(gpt_response):
    lines = gpt_response.split('\n')
    topics = []
    counter = 0
    for line in lines:
        if counter >= NUMBER_OF_CHAPTERS:
            break
        if line == '':
            continue # Skip blank lines
        if line[0].isdigit():
            topics.append(line.title()) # if it starts with a digit, it's probably a good subtopic
            counter += 1
        

    print("**********************")
    print("List of Topics:")
    print("**********************")
    for topic in topics:
        print(topic)
    print("**********************")


    return topics

def ask_chat_gpt_and_get_response(system_content, user_content):
    system_content = system_content.strip()
    user_content = user_content.strip()
    if DEBUG:
        return f"Blah blah blah. Example text for {system_content} and {user_content}"
    
    print("************************************")
    print("ASKING CHAT GPT")
    print("************************************")
    print(f"System Prompt:\n{system_content}")
    print("\n")
    print(f"User Prompt:\n{user_content}")
    print("************************************")
    print("Please be patient....")

    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_content,
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ]
        )
        result = response.choices[0].message['content']
        print(f"Done! Here is the result:\n{result}")
        print("**************************************")
        return response.choices[0].message['content']
    except:
        return ask_chat_gpt_and_get_response(system_content, user_content)


def get_chapter_for_subtopic(subtopic):
    print(f"Start writing chapter text for {subtopic}")
    system_content = f"You are writing a chapter of a text book. The user will give you a topic of the chapter. Please write a textbook chapter explaining the topic. Assume a {EDUCATION_LEVEL} level. Your response should be formatted as HTML."
    results = ask_chat_gpt_and_get_response(system_content, subtopic)
    print(f"End writing chapter text for {subtopic}")
    return results


def get_discussion_questions_for_subtopic(subtopic):
    print(f"Start DISCUSSION QUESTIONS for {subtopic}")
    system_content = f"Imagine you are teaching a college level class about {subtopic}. Write {NUMBER_OF_DISCUSSION_QUESTIONS} discussion questions about {subtopic} for the class. The {NUMBER_OF_DISCUSSION_QUESTIONS} questions should be numbered. The response should be formatted as an HTML page."
    results = ask_chat_gpt_and_get_response(system_content, system_content)
    print(f"End DISCUSSION QUESTIONS for {subtopic}")
    return results

def get_test_prep_questions_for_subtopic(subtopic):
    print(f"Start TEST PREP QUESTIONS for {subtopic}")
    system_content = f"Imagine you are teaching a college level class about {subtopic}. Write {NUMBER_OF_DISCUSSION_QUESTIONS} questions about {subtopic} that might appear on a test for the class. The {NUMBER_OF_DISCUSSION_QUESTIONS} questions should be numbered. The response should be formatted as an HTML page."
    results = ask_chat_gpt_and_get_response(system_content, system_content)
    print(f"End TEST PREP QUESTIONS for {subtopic}")
    return results

def get_resources_for_subtopic(subtopic):
    print(f"Start ADDITIONAL_RESOURCES for {subtopic}")
    system_content = f"Imagine you teaching a college level class about {subtopic}. Write a list of {NUMBER_OF_ADDITIONAL_RESOURCES} additional resources about {subtopic} that a student could use to learn more. The {NUMBER_OF_DISCUSSION_QUESTIONS} additional resources should be numbered. The response should be formatted as an HTML page."
    results = ask_chat_gpt_and_get_response(system_content, system_content)
    print(f"End ADDITIONAL_RESOURCES for {subtopic}")
    return results

from pymongo import MongoClient
def test_putting_something_in_database():
    print('Starting test_putting_something_in_database()')
    test_data = {
        "prompt": "testing 123",
        "response": "fake response",
    }

    # CONNECTION_STRING = "mongodb+srv://user:pass@localhost/myFirstDatabase"
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING)
    db = client['textbook']
    collection = db['test_collection_1']
    collection.insert_one(test_data)

    cursor = collection.find({})
    for document in cursor:
          print(document)

    print('End test_putting_something_in_database()')
    return

def save_a_new_book_to_our_books_table(book):
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING)
    db = client['textbook']
    books_collection = db['books']
    result = books_collection.insert_one(book)
    new_book_id = str(result.inserted_id)

    found_new_book = books_collection.find_one({"_id": ObjectId(new_book_id)})
    books_collection.update_one({"_id": ObjectId(new_book_id)}, {"$set": {"book_id": new_book_id}})

    return new_book_id
    

def generate_textbook_from_user_input(raw_input):
    print('^^^^^^^^^^^^^^^^^^^')
    print('Start Generating Textbook Function')
    print('^^^^^^^^^^^^^^^^^^^')
    
    gpt_response = ask_gpt_to_list_topics(raw_input)
    subtopics = divide_response_into_subtopics(gpt_response)
    print(subtopics)
    subtopic_chapters = []
    for subtopic in subtopics:
        subtopic_chapter = get_chapter_for_subtopic(subtopic)
        subtopic_discussion_questions = get_discussion_questions_for_subtopic(subtopic)
        test_prep_questions = get_test_prep_questions_for_subtopic(subtopic)
        resources = get_resources_for_subtopic(subtopic)
        new_chapter = {
            'chapter_title': subtopic,
            'chapter_content': subtopic_chapter,
            'subtopic_discussion_questions': subtopic_discussion_questions,
            'test_prep_questions': test_prep_questions,
            'resources': resources,
        }
        subtopic_chapters.append(new_chapter)
    book_title = raw_input.title()
    textbook = {
        'title': f"{book_title}: A Humble Explanation",
        'chapters': subtopic_chapters, 
    }
    print(f"textbook: {textbook}")
    new_book_id = save_a_new_book_to_our_books_table(textbook)
    textbook['book_id'] = new_book_id

    print('^^^^^^^^^^^^^^^^^^^')
    print('End Generating Textbook Function')
    print('^^^^^^^^^^^^^^^^^^^')
    return textbook


def get_body_contents_from_html_file(html_file_contents_as_str):
    if not html_file_contents_as_str:
        return ''
    html_soup = BeautifulSoup(html_file_contents_as_str, 'html.parser')
    body_element = html_soup.body
    if body_element: 
        body_contents = body_element.contents
        only_nonempty_lines = list(filter(lambda x: x != '\n', body_contents))
        only_nonempty_lines_as_strings = list(map(lambda x: str(x), only_nonempty_lines))
        return mark_safe(''.join(only_nonempty_lines_as_strings))
    return ''


def ask_chat_gpt_for_book_topics():
    print('^^^^^^^^^^^^^^^^^^^')
    print('Start Generating a List of Book Topics function')
    print('^^^^^^^^^^^^^^^^^^^')



    existing_book_titles = get_str_of_all_existing_book_titles()
    context = f"Imagine you are a college student. You want to become incredibly wealthy, happy, successful, wise, smart. Please generate a list of {NUMBER_OF_AUTO_SUGGESTED_BOOK_IDEAS} topics to study to help you achieve your life goals. These topics should be practical. However, the topics should NOT be related to things in this list: {existing_book_titles}. Format the list with each topic on its own line. And number the list."
    results = ask_chat_gpt_and_get_response(context, context)

    print('^^^^^^^^^^^^^^^^^^^')
    print('END Generating a List of Book Topics function')
    print('^^^^^^^^^^^^^^^^^^^')

    return results


def get_a_list_of_all_book_ids():
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING)
    db = client['textbook']
    books_collection = db['books']

    all_book_ids = []
    for book in books_collection.find({}):
        book_id = str(book.get('_id', ''))
        all_book_ids.append(book_id)

    return all_book_ids

def get_str_of_all_existing_book_titles():
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING)
    db = client['textbook']
    books_collection = db['books']

    all_books_in_db = books_collection.find({})
    all_titles = []
    for book in all_books_in_db:
        book_title = book.get('title', '')
        book_title = find_before_substring(book_title, ': A Humble Explanation')
        book_title = book_title.strip()
        all_titles.append(book_title)

    retVal = ', '.join(all_titles)
    return retVal


import re
import string

def remove_starting_digits_and_punct(s):
    return re.sub(r"^[0-9" + string.punctuation + "]+", "", s)


def find_before_substring(main_string, substring):
    """
    This function returns everything in the first string that occurs before the second string. 
    If the second string is not in the first string, it returns all of the first string.
    
    Parameters:
    main_string (str): The main string in which to find the substring.
    substring (str): The substring to find in the main string.

    Returns:
    str: The part of the main string before the substring, or the whole main string if the substring is not found.
    """
    # Find the index of the substring in the main string
    index = main_string.find(substring)

    # If the substring is not found, return the whole main string
    if index == -1:
        return main_string

    # If the substring is found, return the part of the main string before it
    else:
        return main_string[:index]
    

def parse_list_of_book_topics_into_list(gpt_response):
    lines = gpt_response.split('\n')
    topics = []
    for line in lines:
        if line == '':
            continue # Skip blank lines
        if line[0].isdigit():
            line = remove_starting_digits_and_punct(line)
            topics.append(line.title()) # if it starts with a digit, it's probably a good subtopic
    return topics        


def generate_a_book_for_each_item_in_list(list_of_book_ideas):
    for book_idea in list_of_book_ideas:
        generate_textbook_from_user_input(book_idea)


def generate_auto_books():
    book_ideas = ask_chat_gpt_for_book_topics()
    generate_a_book_for_each_item_in_list(parse_list_of_book_topics_into_list(book_ideas))

def delete_by_id():
    id_to_delete = "6498a9a8d5ceabbbd3192c6a"
    CONNECTION_STRING = "mongodb://localhost:27017/"
    client = MongoClient(CONNECTION_STRING)
    db = client['textbook']
    books_collection = db['books']
    books_collection.delete_one({"_id": ObjectId(id_to_delete)})


def ask_chat_gpt_for_single_new_book_idea():
    print('^^^^^^^^^^^^^^^^^^^')
    print('Start Generating a List of Book Topics function')
    print('^^^^^^^^^^^^^^^^^^^')



    existing_book_titles = get_str_of_all_existing_book_titles()
    context = f"Imagine you are a college student. You want to become incredibly wealthy, happy, successful, wise, smart. Please generate a list of two topics to study to help you achieve your life goals. These topics should be practical. However, the topics should NOT be related to things in this list: {existing_book_titles}. Format the list with each topic on its own line. And number the list."
    results = ask_chat_gpt_and_get_response(context, context)

    print('^^^^^^^^^^^^^^^^^^^')
    print('END Generating a List of Book Topics function')
    print('^^^^^^^^^^^^^^^^^^^')

    results = parse_list_of_book_topics_into_list(results)
    if len(results) > 1: 
        results = results[0:1]
    return results



def auto_book_idea_one_at_a_time():
    counter = 0
    while counter < 5:
        single_idea = ask_chat_gpt_for_single_new_book_idea()
        generate_a_book_for_each_item_in_list(single_idea)
        counter = counter + 1


import requests

def save_url_html_to_file(url, file_path):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # If the GET request is successful, the status code will be 200
    if response.status_code == 200:
        # Get the content of the response
        html_content = response.text
        
        # Open the file in write mode and write the HTML content to it
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
    else:
        print(f"Failed to get HTML from URL. Status code: {response.status_code}")



def given_a_book_id_return_the_book_url(book_id):
    return f'http://127.0.0.1:8000/book?id={book_id}'

def given_a_book_id_return_a_file_path(book_id):
    return f'/Users/kevinverre/code/exported_html/{book_id}.html'

def scrape_all_books():
    book_ids = get_a_list_of_all_book_ids()
    book_ids = book_ids[0:1]
    for book_id in book_ids:
        book_url = given_a_book_id_return_the_book_url(book_id)
        book_path = given_a_book_id_return_a_file_path(book_id)
        save_url_html_to_file(book_url, book_path)
        print(f"URL:\n{book_url}\nPATH:\n{book_path}")




def main():
    print("starting main()")
    #test_putting_something_in_database()
    print("Ending main()")
    return

    # while True:
    raw_input = get_user_input_from_command_line()
    gpt_response = ask_gpt_to_list_topics(raw_input)
    print("GPT-3.5 response:")
    print(f"{gpt_response}")
    subtopics = divide_response_into_subtopics(gpt_response)
    for subtopic in subtopics:
        print("\n\n")
        print(f"CHAPTER: {subtopic}")
        subtopic_chapter = get_chapter_for_subtopic(subtopic)
        print(f"{subtopic_chapter}")

# if __name__ == "__main__":
#     main()


