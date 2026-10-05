#!/usr/bin/env -S poetry run python

import os
import sys

from openai import OpenAI

api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    sys.exit("OPENAI_API_KEY environment variable is required")

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(api_key=api_key)

# Non-streaming:
print("----- standard request -----")
completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        },
    ],
)
print(completion.choices[0].message.content)

# Streaming:
print("----- streaming request -----")
stream = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "user",
            "content": "How do I output all files in a directory using Python?",
        },
    ],
    stream=True,
)
for chunk in stream:
    if not chunk.choices:
        continue

    print(chunk.choices[0].delta.content, end="")
print()

# Response headers:
print("----- custom response headers test -----")
response = client.chat.completions.with_raw_response.create(
    model="gpt-4",
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
)
completion = response.parse()
print(response.request_id)
print(completion.choices[0].message.content)
