import ollama
from pydantic import BaseModel

class SearchQueries(BaseModel):
    queries: list[str]

def GenerateQueries(message):
    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": message
            }
        ]
        ,format=SearchQueries.model_json_schema()
    )
    data = SearchQueries.model_validate_json(response["message"]["content"])
    return data
print(GenerateQueries("give 5 queries for video games").queries)

