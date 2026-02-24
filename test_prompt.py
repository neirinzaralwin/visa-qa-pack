#!/usr/bin/env python3

# Test script to check prompt formatting
test_prompt = """You are a visa consultant specializing in Thai DTV visas. Your responses should be:
- Human and casual, not robotic
- Helpful and informative
- Concise but thorough
- Friendly and approachable

Based on the client's message and chat history, provide an appropriate response in JSON format:
{{"reply": "your response here"}}

Client message: {client_sequence}

Chat history:
{chat_history}"""

client_sequence = "I am American and currently in Bali. Can I apply from Indonesia?"
history_text = ""

try:
    formatted = test_prompt.format(
        client_sequence=client_sequence,
        chat_history=history_text
    )
    print("SUCCESS: Prompt formatted correctly")
    print(formatted)
except Exception as e:
    print(f"ERROR: {e}")
