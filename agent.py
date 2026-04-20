from openai import OpenAI
from dotenv import load_dotenv
from database.setup import (
    get_all_medications, 
    create_medication,
    delete_medication,
    setup_db
)

import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
)

system_content = """You are a very sarcastic AI medication agent where you 
                    can make queries to a database to obtain the user's medications.
                    You main function right now:
                    1. If the user asks for medications, output the letter 'r' as a flag, THAT IS IT
                    2. If the user asks to create a medication, there is 2 required parameters, name and dosage,
                    both of these are required, if there is one missing say it is missing, else just simply output
                    this - 'c|{name}|{dosage}' 
                    3. If the user asks to delete a medication, there is 2 required parameters as well, name and
                    dosage, both of these are required, if there is a one missing say it is missing, else just simply
                    output this - 'd|{name}|{dosage}'
                    """

system_message = {
    "role": "system",
    "content": system_content
}

setup_db()

while True:
    user_input = input("User: ")

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        messages=[
            system_message,
            {"role": "user", "content": user_input}
        ],
    )

    clean_response = response.choices[0].message.content.strip()

    if (clean_response == "r"):
        output = get_all_medications()
        print(f"Medication Agent: {output}")
    elif(clean_response.startswith("c")):
        arr = clean_response.split("|")
        medication_name = arr[1]
        medication_dosage = arr[2]
        create_medication(medication_name, medication_dosage)
        print("Medication Agent: Medication Successfully Recorded")
    elif(clean_response.startswith("d")):
        arr = clean_response.split("|")
        medication_name = arr[1]
        medication_dosage = arr[2]
        delete_medication(medication_name, medication_dosage)
        print("Medication Agent: Medication Successfully Deleted")
    else:
        print(f"Medication Agent: {clean_response}")