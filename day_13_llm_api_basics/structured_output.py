from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class RAGExplanation(BaseModel):
    definition: str
    purpose: str
    example: str


client = OpenAI()


response = client.responses.parse(
    model="gpt-5.6-luna",
    input=(
        "Explain RAG for a beginner. "
        "Give a definition, its main purpose, "
        "and one simple example."
    ),
    text_format=RAGExplanation
)


result = response.output_parsed


print("Definition:", result.definition)
print("Purpose:", result.purpose)
print("Example:", result.example)
