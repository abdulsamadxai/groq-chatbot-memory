# 🧠 Chatbot with Memory - Now it Remembers You

In the last guide we built a basic chatbot. It worked but had one big problem - it forgot everything after every message. This guide fixes that. We add **memory** so the AI remembers the whole conversation.

The only real change? One list called `chat_history`.

---

## Table of Contents

1. [What is the problem we are fixing?](#what-is-the-problem-we-are-fixing)
2. [What changed from last time?](#what-changed-from-last-time)
3. [The full code](#the-full-code)
4. [Line by line - what each part does](#line-by-line---what-each-part-does)
   - [Part 1 - chat_history list](#part-1---chat_history-list)
   - [Part 2 - Adding your message](#part-2---adding-your-message)
   - [Part 3 - Sending the full history](#part-3---sending-the-full-history)
   - [Part 4 - Saving the bot reply](#part-4---saving-the-bot-reply)
5. [How memory actually works](#how-memory-actually-works)
6. [How it all flows](#how-it-all-flows)
7. [Word List](#word-list)

---

## What is the problem we are fixing?

The old chatbot sent only your current message to the AI every time. So the AI had no idea what happened before.

```mermaid
flowchart TD
    A["❌ Old chatbot - no memory"]:::label

    A1["You: My name is Samad"]:::blue --> B1["Bot: Nice to meet you Samad!"]:::green
    B1 --> A2["You: What is my name?"]:::blue --> B2["Bot: I don't know your name 🤔\nnobody told me"]:::red

    classDef label fill:#3a0f0f,stroke:#ef4444,color:#fca5a5,font-weight:bold
    classDef blue fill:#1e3a5f,stroke:#4a8fd4,color:#a8d4ff
    classDef green fill:#1a3a2a,stroke:#34d399,color:#6ee7b7
    classDef red fill:#3a0f0f,stroke:#ef4444,color:#fca5a5
```

The new chatbot saves everything and sends the full conversation every time.

```mermaid
flowchart TD
    A["✅ New chatbot - with memory"]:::label

    A1["You: My name is Samad"]:::blue --> B1["Bot: Nice to meet you Samad!"]:::green
    B1 --> A2["You: What is my name?"]:::blue --> B2["Bot: Your name is Samad!"]:::green

    classDef label fill:#1a3a2a,stroke:#34d399,color:#6ee7b7,font-weight:bold
    classDef blue fill:#1e3a5f,stroke:#4a8fd4,color:#a8d4ff
    classDef green fill:#1a3a2a,stroke:#34d399,color:#6ee7b7
```

---

## What changed from last time?

Only 3 things changed. Everything else is exactly the same.

| What | Old code | New code |
|------|----------|----------|
| Chat history | did not exist | `chat_history = []` created |
| Messages sent to API | only current message | full `chat_history` list |
| Bot reply | printed and forgotten | saved into `chat_history` too |

---

## The full code

```python
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
```

---

## Line by line - what each part does

### Part 1 - chat_history list

```python
chat_history = []
```

This is the only new setup line. It creates an empty list before the loop starts.

This list will grow with every message - yours and the bot's. By the end of a conversation it looks like this:

```python
[
    {"role": "user",      "content": "My name is Samad"},
    {"role": "assistant", "content": "Nice to meet you Samad!"},
    {"role": "user",      "content": "What is my name?"},
    {"role": "assistant", "content": "Your name is Samad!"}
]
```

Each item in the list is a dictionary with two keys - `role` and `content`.

| Key | What it means |
|-----|--------------|
| `role` | who said this - either `"user"` or `"assistant"` |
| `content` | what was actually said |

The AI reads this list and knows exactly who said what and in what order.

---

### Part 2 - Adding your message

```python
chat_history.append(
    {
        "role": "user",
        "content": user_input
    }
)
```

Before sending anything to the AI, we first save your message into `chat_history`.

`.append()` adds a new item to the end of the list. So every time you type something, it gets added as a new dictionary with `role: user`.

```mermaid
flowchart LR
    A["💬 You type\n'What is Python?'"]:::blue -->|append| B["📋 chat_history\n...\n{'role': 'user', 'content': 'What is Python?'}"]:::purple

    classDef blue fill:#1e3a5f,stroke:#4a8fd4,color:#a8d4ff
    classDef purple fill:#2d1b4e,stroke:#8b5cf6,color:#c4b5fd
```

---

### Part 3 - Sending the full history

```python
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=chat_history
)
```

Notice what changed here from the old code.

Old code sent only the current message:
```python
messages=[{"role": "user", "content": user_input}]
```

New code sends the whole history:
```python
messages=chat_history
```

This is how the AI remembers. We are not storing memory inside the AI - we are just sending it the full conversation every single time. The AI reads it all fresh and replies knowing everything that was said before.

```mermaid
flowchart TD
    HIST["📋 chat_history\nmessage 1 - user\nmessage 2 - assistant\nmessage 3 - user\nmessage 4 - assistant\nmessage 5 - user 👈 latest"]:::purple

    HIST -->|sent to Groq every time| API["🌐 Groq API\nreads full history\nunderstands context"]:::blue
    API --> REPLY["🤖 Smart reply\nknows everything said before"]:::green

    classDef purple fill:#2d1b4e,stroke:#8b5cf6,color:#c4b5fd
    classDef blue fill:#1e3a5f,stroke:#4a8fd4,color:#a8d4ff
    classDef green fill:#1a3a2a,stroke:#34d399,color:#6ee7b7
```

---

### Part 4 - Saving the bot reply

```python
bot_reply = response.choices[0].message.content

chat_history.append(
    {
        "role": "assistant",
        "content": bot_reply
    }
)

print("Bot:", bot_reply)
```

After we get the reply we do two things.

First we save it in `bot_reply` so we can use it twice without writing `response.choices[0].message.content` two times.

Then we append it to `chat_history` with `role: assistant`. This is important - if we skip this step, the AI will not remember its own previous answers either.

```mermaid
flowchart LR
    A["📥 response comes back\nfrom Groq"]:::blue -->|extract text| B["bot_reply\n'Python is a language...'"]:::teal
    B -->|append to history| C["📋 chat_history\n{'role': 'assistant',\n'content': 'Python is...'}"]:::purple
    B -->|print| D["🖨️ Bot: Python is a language..."]:::green

    classDef blue fill:#1e3a5f,stroke:#4a8fd4,color:#a8d4ff
    classDef teal fill:#0f3030,stroke:#2dd4bf,color:#99f6e4
    classDef purple fill:#2d1b4e,stroke:#8b5cf6,color:#c4b5fd
    classDef green fill:#1a3a2a,stroke:#34d399,color:#6ee7b7
```

---

## How memory actually works

Here is the important thing to understand. **The AI has no memory of its own.**

Every time you send a message, the AI starts completely fresh. It does not store your conversation anywhere. We are the ones keeping the list and re-sending everything each time.

```mermaid
flowchart TD
    TURN1["🔁 Turn 1"]:::label
    TURN1 --> S1["We send: message 1"]:::blue --> R1["AI replies: reply 1"]:::green

    TURN2["🔁 Turn 2"]:::label
    TURN2 --> S2["We send: message 1 + reply 1 + message 2"]:::blue --> R2["AI replies: reply 2"]:::green

    TURN3["🔁 Turn 3"]:::label
    TURN3 --> S3["We send: message 1 + reply 1 + message 2 + reply 2 + message 3"]:::blue --> R3["AI replies: reply 3"]:::green

    classDef label fill:#252535,stroke:#4a4a6a,color:#c0c0d8,font-weight:bold
    classDef blue fill:#1e3a5f,stroke:#4a8fd4,color:#a8d4ff
    classDef green fill:#1a3a2a,stroke:#34d399,color:#6ee7b7
```

Every turn we send a little more. The list keeps growing. That is why a very long conversation costs more - more tokens are being sent each time.

---

## How it all flows

```mermaid
flowchart TD
    START["▶️ Code starts"]:::gray
    START --> LOAD["📄 .env loaded\nGroq client ready"]:::blue
    LOAD --> HIST["📋 chat_history = empty list"]:::purple
    HIST --> LOOP["🔁 Loop begins"]:::gray
    LOOP --> INPUT["💬 You type something"]:::blue
    INPUT --> EXIT{"typed exit?"}:::teal
    EXIT -->|yes| BYE["👋 Loop stops"]:::red
    EXIT -->|no| APP1["📋 Append your message\nrole: user"]:::purple
    APP1 --> API["🌐 Send full chat_history\nto Groq API"]:::blue
    API --> WAIT["⏳ AI reads everything\nand replies"]:::gray
    WAIT --> SAVE["💾 Save reply in bot_reply"]:::teal
    SAVE --> APP2["📋 Append bot reply\nrole: assistant"]:::purple
    APP2 --> PRINT["🖨️ Print the reply"]:::green
    PRINT --> LOOP

    classDef gray fill:#252535,stroke:#4a4a6a,color:#c0c0d8
    classDef blue fill:#1e3a5f,stroke:#4a8fd4,color:#a8d4ff
    classDef purple fill:#2d1b4e,stroke:#8b5cf6,color:#c4b5fd
    classDef teal fill:#0f3030,stroke:#2dd4bf,color:#99f6e4
    classDef green fill:#1a3a2a,stroke:#34d399,color:#6ee7b7
    classDef red fill:#3a0f0f,stroke:#ef4444,color:#fca5a5
```

---

## Word List

| Word | Simple meaning |
|------|--------------|
| `chat_history` | a list that stores all messages in order |
| `.append()` | adds a new item to the end of a list |
| `role` | who said a message - either user or assistant |
| `content` | the actual text of the message |
| `bot_reply` | a variable to hold the AI's reply text |
| Context | everything the AI can read in one go |
| Token | a small piece of text - sending more history means more tokens |

---

## What's Next?

```mermaid
flowchart TD
    A["✅ You finished this guide\nyour chatbot now remembers!"]:::done
    A --> B["🎭 Next - Add a System Prompt\ngive your chatbot a personality and a role"]:::blue

    classDef done fill:#1a3a2a,stroke:#34d399,color:#6ee7b7
    classDef blue fill:#1e3a5f,stroke:#4a8fd4,color:#a8d4ff
```

---

*Made by Abdul Samad*
