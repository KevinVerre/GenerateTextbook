import openai
import os
from secret_values import MY_SECRET_CHAT_GPT_KEY_PLS_DONT_STEAL_THIS_THX

openai.api_key = MY_SECRET_CHAT_GPT_KEY_PLS_DONT_STEAL_THIS_THX  # replace with your OpenAI API key

def get_user_input_plus_our_prompt():
    print("Enter a topic you want to learn about. Then hit enter:")
    the_user_response = input("")
    return f"{the_user_response} for high school students"
    # return "Evolutionary biology for high school students"
    # return input("Enter your message: ")

def send_to_gpt(user_input_plus_our_prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are writing a text book. The user will give you a topic. Please write five topics and keywords that are important to the topic that the user input."
            },
            {
                "role": "user",
                "content": user_input_plus_our_prompt
            }
        ]
    )
    return response.choices[0].message['content']

def divide_response_into_subtopics(gpt_response):
    return gpt_response.split('\n')

def get_chapter_for_subtopic(subtopic):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are writing a chapter of a text book. The user will give you a topic of the chapter. Please write a textbook chapter explaining the topic. Assume a high school level."
            },
            {
                "role": "user",
                "content": subtopic
            }
        ]
    )
    return response.choices[0].message['content']

def main():
    # while True:
    user_input_plus_our_prompt = get_user_input_plus_our_prompt()
    gpt_response = send_to_gpt(user_input_plus_our_prompt)
    print("GPT-3.5 response:")
    print(f"{gpt_response}")
    subtopics = divide_response_into_subtopics(gpt_response)
    for subtopic in subtopics:
        print("\n\n")
        print(f"CHAPTER: {subtopic}")
        subtopic_chapter = get_chapter_for_subtopic(subtopic)
        print(f"{subtopic_chapter}")

if __name__ == "__main__":
    main()
