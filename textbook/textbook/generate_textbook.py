import openai
import os
import sys
from django.utils.safestring import mark_safe

sys.path.append("..")
from secret_values import MY_SECRET_CHAT_GPT_KEY_PLS_DONT_STEAL_THIS_THX


openai.api_key = MY_SECRET_CHAT_GPT_KEY_PLS_DONT_STEAL_THIS_THX  # replace with your OpenAI API key


NUMBER_OF_CHAPTERS = 1

def get_user_input_from_command_line():
    print("Enter a topic you want to learn about. Then hit enter:")
    the_user_response = input("")
    return the_user_response


def get_user_input_plus_our_prompt(the_user_response):
    return f"{the_user_response} for high school students"
    # return "Evolutionary biology for high school students"
    # return input("Enter your message: ")

def ask_gpt_to_list_topics(raw_user_input):
    my_prompt = f"Imagine you are going to write a textbook about {raw_user_input}. Generate a list of ten topics related to {raw_user_input}. Return a list where each item in the list starts with a number."
    print("**********************")
    print("Asking GPT To Generate a list of Topics")
    print("**********************")
    print(my_prompt)
    print("**********************")

    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": my_prompt
            },
            {
                "role": "user",
                "content": my_prompt
            }
        ]
    )
    return response.choices[0].message['content']

def divide_response_into_subtopics(gpt_response):
    lines = gpt_response.split('\n')
    topics = []
    counter = 0
    for line in lines:
        if counter > NUMBER_OF_CHAPTERS:
            break
        if line == '':
            continue # Skip blank lines
        if line[0].isdigit():
            topics.append(line) # if it starts with a digit, it's probably a good subtopic

        counter += 1

    print("**********************")
    print("List of Topics:")
    print("**********************")
    for topic in topics:
        print(topic)
    print("**********************")


    return topics

def get_chapter_for_subtopic(subtopic):
    print(f"Trying to create a chapter about '{subtopic}'. Please be patient...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are writing a chapter of a text book. The user will give you a topic of the chapter. Please write a textbook chapter explaining the topic. Assume a high school level. Your response should be formatted as HTML."
            },
            {
                "role": "user",
                "content": subtopic
            }
        ]
    )
    result = response.choices[0].message['content']
    print(f"Done! Here is the result: {result}")
    return response.choices[0].message['content']


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



def generate_textbook_from_user_input(raw_input):
    gpt_response = ask_gpt_to_list_topics(raw_input)
    print("GPT-3.5 response:")
    print(f"{gpt_response}")
    subtopics = divide_response_into_subtopics(gpt_response)
    print(subtopics)
    subtopic_chapters = []
    for subtopic in subtopics:
        subtopic_chapter = get_chapter_for_subtopic(subtopic)
        new_chapter = {
            'chapter_title': subtopic,
            'chapter_content': mark_safe(subtopic_chapter),
        }
        subtopic_chapters.append(new_chapter)
    textbook = {
        'title': f"{raw_input.capitalize()}: A Humble Explanation",
        'chapters': subtopic_chapters, 
    }
    print(f"textbook: {textbook}")
    return textbook

    
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


