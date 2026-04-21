from openai import OpenAI
from dotenv import load_dotenv
from app.services.medication_service import MedicationService

import os
import json

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
)

system_content = """
You are a sarcastic AI medication assistant.

You must respond ONLY with valid JSON.

Available actions:
1. get_all_medications
2. create_medication
3. delete_medication
4. get_medication_by_name
5. get_medication_by_dosage
6. get_medication_by_name_and_dosage
7. ask_for_missing_info

Examples:

{"action": "get_all_medications"}

{"action": "create_medication", "name": "Ibuprofen", "dosage":"200mg"}

{"action":"delete_medication","name":"Ibuprofen","dosage":"200mg"}

{"action":"get_medication_by_name","name":"Ibuprofen"}

{"action":"get_medication_by_dosage","dosage":"200mg"}

{"action":"get_medication_by_name_and_dosage","name":"Ibuprofen","dosage":"200mg"}

{"action":"ask_for_missing_info","message":"Please provide the dosage."}

Do not include markdown.
Do not include explanations outside JSON.
"""

system_message = {
    "role": "system",
    "content": system_content
}

while True:
    user_input = input("User: ").strip()

    if user_input.lower() in ["exit", "quit"]:
        print("TERMINATING PROCESS")
        break

    try:
        response = client.chat.completions.create(
            model="nvidia/nemotron-3-super-120b-a12b:free",
            messages=[
                system_message,
                {"role": "user", "content": user_input}
            ],
        )

        content = response.choices[0].message.content.strip()
        data = json.loads(content)
        
        agent = MedicationService()
        action = data.get("action")

        if action == "get_all_medications":
            output = agent.get_all_medications()
            print(f"Medication Agent: {output}")

        elif action == "create_medication":
            name = data.get("name")
            dosage = data.get("dosage")

            if not name or not dosage:
                print("Medication Agent: Missing name or dosage")
                continue

            agent.create_medication(name, dosage)
            print("Medication Agent: Medication successfully recorded")
        
        elif action == "delete_medication":
            name = data.get("name")
            dosage = data.get("dosage")

            if not name or not dosage:
                print("Medication Agent: Missing name or dosage")
                continue

            deleted = agent.delete_medication(name, dosage)

            if deleted:
                print("Medication Agent: Medication successfully deleted")
            else:
                print("Medication Agent: No matching medication found")
        
        elif action == "get_medication_by_name":
            name = data.get("name")
            if not name:
                print("Medication Agent: Missing medication name")
                continue

            output = agent.get_medication_by_name(name)
            print(f"Medication Agent: {output}")

        elif action == "get_medication_by_dosage":
            dosage = data.get("dosage")
            if not dosage:
                print("Medication Agent: Missing medication dosage")
                continue

            output = agent.get_medication_by_dosage(dosage)
            print(f"Medication Agent: {output}")
        
        elif action == "get_medication_by_name_and_dosage":
            name = data.get("name")
            dosage = data.get("dosage")

            if not name or not dosage:
                print("Medication Agent: Missing name or dosage")
                continue

            output = agent.get_medication_by_name_and_dosage(dosage)
            print(f"Medication Agent: {output}")
        
        elif action == "ask_for_missing_info":
            print(f"Medication Agent: {data.get('message', 'Missing Information')}")
        
        else:
            print("Medication Agent: Unknown action returned by model")
        

    except json.JSONDecodeError:
        print("Medication Agent: Model did not return valid JSON.")
    except Exception as error:
        print(f"Medication Agent: Error - {error}")

    