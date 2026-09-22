from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(
    BASE_DIR / ".env"
)


client = OpenAI()


# response = client.responses.create(
#     model="gpt-5.6-luna",
#     instructions=(
#         "You are a concise technical tutor."
#     ),
#     input=[
#         {
#             "role":"user",
#             "content":"What is RAG?"
#         },
#         {
#             "role":"assistant",
#             "content":(
#                 "RAG combines retrieval "
#                 "with languange generation."
#             )
#         },
#         {
#             "role":"user",
#             "content":(
#                 "Why is retrieval useful?"
#             )
#         }
#     ]
# )

# print(response.output_text)
# print("Input tokens:", response.usage.input_tokens)
# print("Output tokens:", response.usage.output_tokens)
# print("Total tokens:", response.usage.total_tokens)
