import ollama


def GenerateAnswer(prompt, model="qwen3:4b"):
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response["message"]["content"]