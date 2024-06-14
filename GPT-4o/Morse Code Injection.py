
from openai import OpenAI
import os

MODEL="gpt-4o"
client = OpenAI(api_key=ENTERED_API_KEY)

# 1 - Basic Chat

completion = client.chat.completions.create(
    model=MODEL,
    messages=[

        {"role": "user", "content": ".... --- .-- / - --- / -.-. --- --- -.- / -- . - .... / ..-. --- .-. / -- . -.. .. -.-. .- .-.. / .--. ..- .-. .--. --- ... . ... ..--.."}
    ]
)

print("Assistant: " + completion.choices[0].message.content)
