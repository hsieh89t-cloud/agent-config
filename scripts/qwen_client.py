import os
import sys
from openai import OpenAI

BASE_URL = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope-intl.aliyuncs.com/compatible-mode/v1")
DEFAULT_MODEL = os.getenv("DASHSCOPE_MODEL", "qwen2.5-7b-instruct")

client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url=BASE_URL,
)

def chat(prompt: str, model: str = DEFAULT_MODEL, temperature: float = 0.7) -> str:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    return resp.choices[0].message.content

def main():
    if len(sys.argv) < 2:
        print("Usage: qwen_client.py \"<prompt>\"")
        print("Env: DASHSCOPE_API_KEY, DASHSCOPE_MODEL (default qwen2.5-7b-instruct), DASHSCOPE_BASE_URL")
        sys.exit(1)
    prompt = sys.argv[1]
    print(chat(prompt))

if __name__ == "__main__":
    main()
