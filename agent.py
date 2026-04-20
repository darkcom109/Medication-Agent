from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPEN_ROUTER_API_KEY"),
)

system_message = {
    "role": "system",
    "content": "You are a very basic chatbot. Respond in short sentences."
}

while True:
    user_input = input("User: ")

    response = client.chat.completions.create(
        model="nvidia/nemotron-3-super-120b-a12b:free",
        messages=[
            system_message,
            {"role": "user", "content": user_input}
        ],
    )

    print("Medication Agent:", response.choices[0].message.content)