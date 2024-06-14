import base64
from openai import OpenAI

MODEL = "gpt-4o"
client = OpenAI(api_key=ENTERED_API_KEY)

IMAGE_PATH = "trump5.png"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


base64_image = encode_image(IMAGE_PATH)

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}
             }
        ]}
    ],
    temperature=0.0,
)

print(response.choices[0].message.content)
