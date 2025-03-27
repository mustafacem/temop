import openai
import base64
from openai import OpenAI
import requests

import os 



openai_api = os.getenv("OPENAI_API_KEY")
if openai_api is None:
    raise ValueError("OpenAI key not specified!")

client = OpenAI(api_key=openai_api)

#client = openai.OpenAI(api_key=os.getenv("op.env"))

def ask_chatgpt(question):
    """
    Inference for business proposal generation.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are tasked with helping business proposal creation. Just create the desired part and don't write anything else."},
                {"role": "user", "content": question},
            ]
        )
        # Print response to see its structure
        answer = response.choices[0].message.content 
        return answer
    except Exception as e:
        print(f"Error: {e}")
        return None


def mandays_chatgpt(notes, aspect):
    """
    Guess mandays for the given aspect for pricing estimation in an AI startup.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are tasked with guessing {aspect} for price estimates for an AI startup. You will only receive notes and return an integer—nothing else."},
                {"role": "user", "content": notes},
            ]
        )
        answer = response.choices[0].message.content 
        return answer
    except Exception as e:
        print(f"Error: {e}")
        return None


def checker(item, part):
    """
    AI checks if the provided text is suitable for the given part of a business proposal and recommends changes if needed.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are tasked with checking if the provided text is suitable for the given part of a business proposal. If you think changes should be made, provide your recommendations, but keep them as short as possible."},
                {"role": "user", "content": f"Part of business proposal: {item}. Provided text: {part}."},
            ]
        )
        answer = response.choices[0].message.content 
        return answer
    except Exception as e:
        print(f"Error: {e}")
        return None


def decoder(ocr_output, decoder_prompt):
    """
    Translate OCR output from bad handwriting into readable text.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are tasked with creating readable text from bad OCR handwriting output. Follow these instructions for translation: {decoder_prompt}"},
                {"role": "user", "content": ocr_output},
            ]
        )
        answer = response.choices[0].message.content 
        return answer
    except Exception as e:
        print(f"Error: {e}")
        return None


def process_items(items_dict, notes):
    """
    AI generates necessary parts of the proposal and assigns them to items_dict. User can modify them via prompts.
    """
    use_case_description = ask_chatgpt(f"Generate a use case description from the given notes: {notes}")
    if use_case_description is None:
        print("Failed to generate use case description.")
        return

    print(f"Use case description: {use_case_description}")
    response = input("Would you like to enter a custom use case description? (y/n): ").strip().lower()
    if response == 'y':
        use_case_description = input("Enter the desired use case description: ")

    for item in items_dict:
        task_successful = False
        desired_changes = ""
        while not task_successful:
            prompt = f"{desired_changes} Generate {item} for a business proposal for {use_case_description} from the following notes: {notes}."
            value = ask_chatgpt(prompt)

            if value is None:
                print(f"Failed to generate {item}.")
                continue

            print(f"Assigned value for {item}: {value}")
            print("******************************************************************************************************************************")
            opinion_ai = checker(item, value)

            if opinion_ai is None:
                print("Failed to check AI's opinion on this part.")
                continue

            print(f"As AI, my opinion on this part of the proposal is: {opinion_ai}")

            response = input("Happy with the output? (y/n): ").strip().lower()
            if response == 'y':
                task_successful = True
                items_dict[item] = value
                print(f"Value for {item} confirmed: {value}\n")
            else:
                desired_changes = input(f"Enter desired changes for {item}: ")

    print("Finalized proposal items:")
    for key, value in items_dict.items():
        print(f"{key}: {value}")

