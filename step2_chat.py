"""
STEP 2 - Talk to the AI (no tools yet).

Run:  python step2_chat.py
"""
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY automatically

response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=16000,
    messages=[
        {"role": "user", "content": "Explain what an AI agent is in one sentence."}
    ],
)

# The reply is a list of "content blocks". Print the text ones.
for block in response.content:
    if block.type == "text":
        print(block.text)
