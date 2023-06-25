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
NUMBER_OF_CHAPTERS = 1
EDUCATION_LEVEL = 'simple college'
MODEL = 'gpt-3.5-turbo'
NUMBER_OF_DISCUSSION_QUESTIONS = 'five'
NUMBER_OF_ADDITIONAL_RESOURCES = 'three'

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
    print("**********************")
    print("Asking GPT To Generate a list of Topics")
    print("**********************")
    print(my_prompt)
    print("**********************")
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
    if DEBUG:
        return f"Blah blah blah. Example text for {system_content} and {user_content}"
    
    print("************************************")
    print("ASKING CHAT GPT")
    print("************************************")
    print(f"System Prompt:\n{system_content}")
    print("\n\n")
    print(f"User Prompt:\n{user_content}")
    print("************************************")

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


def get_chapter_for_subtopic(subtopic):
    print(f"Trying to create a chapter about '{subtopic}'. Please be patient...")
    system_content = f"You are writing a chapter of a text book. The user will give you a topic of the chapter. Please write a textbook chapter explaining the topic. Assume a {EDUCATION_LEVEL} level. Your response should be formatted as HTML."
    return ask_chat_gpt_and_get_response(system_content, subtopic)


def get_discussion_questions_for_subtopic(subtopic):
    system_content = f"Imagine you are teaching a college level class about {subtopic}. Write {NUMBER_OF_DISCUSSION_QUESTIONS} discussion questions about {subtopic} for the class. The {NUMBER_OF_DISCUSSION_QUESTIONS} questions should be numbered. The response should be formatted as an HTML page."
    return ask_chat_gpt_and_get_response(system_content, system_content)

def get_test_prep_questions_for_subtopic(subtopic):
    system_content = f"Imagine you are teaching a college level class about {subtopic}. Write {NUMBER_OF_DISCUSSION_QUESTIONS} questions about {subtopic} that might appear on a test for the class. The {NUMBER_OF_DISCUSSION_QUESTIONS} questions should be numbered. The response should be formatted as an HTML page."
    return ask_chat_gpt_and_get_response(system_content, system_content)

def get_resources_for_subtopic(subtopic):
    system_content = f"Imagine you teaching a college level class about {subtopic}. Write a list of {NUMBER_OF_ADDITIONAL_RESOURCES} additional resources about {subtopic} that a student could use to learn more. The {NUMBER_OF_DISCUSSION_QUESTIONS} additional resources should be numbered. The response should be formatted as an HTML page."
    return ask_chat_gpt_and_get_response(system_content, system_content)

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
    gpt_response = ask_gpt_to_list_topics(raw_input)
    print("GPT-3.5 response:")
    print(f"{gpt_response}")
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
    textbook = {
        'title': f"{raw_input.title()}: A Humble Explanation",
        'chapters': subtopic_chapters, 
    }
    print(f"textbook: {textbook}")
    new_book_id = save_a_new_book_to_our_books_table(textbook)
    textbook['book_id'] = new_book_id
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


