import os
from dotenv import load_dotenv
from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
from strands_tools import current_time, python_repl

load_dotenv()

@tool
def letter_counter(word: str, letter: str) -> int:
    return word.lower().count(letter.lower())

litellm_model = LiteLLMModel(
    client_args={
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
    model_id="gpt-4o",
    params={
        "temperature": 0.7,
    }
)

agent = Agent(model=litellm_model, tools=[current_time, python_repl, letter_counter])

message = """
いくつか質問があります。

1. いま日本は何時？
2. その時刻表示の中に「1」はいくつある？
3. ここまで話した内容をPyhtonコードにして。テストしたあとにコード内容を表示して。
"""

agent(message)

