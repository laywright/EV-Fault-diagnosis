from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents="Compose a love poem that explains programming and hitting a stone wall",
    config={
        "system_instruction": "You are a hopeless romantic assistant, skilled at explaining complex systems with flair for easier understanding.",
    },
)

print(response.text)