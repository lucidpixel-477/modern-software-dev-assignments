import os
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

# TODO: Fill this in!
YOUR_SYSTEM_PROMPT = """
You are a deterministic character reversal function.

Your only job is to reverse the user's input character by character.

Critical rules:
- Treat the input as one continuous string of characters.
- Do not split the input into words, prefixes, suffixes, or meaningful parts.
- Do not correct spelling.
- Do not explain.
- Output only the final reversed string.
- The output must contain no spaces, punctuation, quotes, markdown, or labels.
- The output length must exactly equal the input length.

Examples:
Input: abcd
Output: dcba

Input: apple
Output: elppa

Input: dogcat
Output: tacgod

Input: redblue
Output: eulbder

Input: fastapi
Output: ipatsaf

Input: httpstatus
Characters: h t t p s t a t u s
Reversed characters: s u t a t s p t t h
Output: sutatsptth

When given a new input, follow the same character-by-character process and return only the reversed string.
"""

USER_PROMPT = """
Reverse the order of letters in the following word. Only output the reversed word, no other text:

httpstatus
"""


EXPECTED_OUTPUT = "sutatsptth"

def test_your_prompt(system_prompt: str) -> bool:
    """Run the prompt up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

    Prints "SUCCESS" when a match is found.
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = chat(
            model="mistral-nemo:12b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.5},
        )
        output_text = response.message.content.strip()
        if output_text.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {output_text}")
    return False

if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)