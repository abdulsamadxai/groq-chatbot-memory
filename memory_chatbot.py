from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

chat_history = []

print("Chatbot Started (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    chat_history.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=chat_history
    )

    bot_reply = response.choices[0].message.content

    chat_history.append(
        {
            "role": "assistant",
            "content": bot_reply
        }
    )

    print("Bot:", bot_reply)