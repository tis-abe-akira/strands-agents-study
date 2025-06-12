import os
from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
from strands_tools import current_time, python_repl

# Set up LangSmith environment variables
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-api-key"  # Replace with your actual API key
os.environ["LANGCHAIN_PROJECT"] = "strands-agents-project"  # Replace with your project name

@tool
def letter_counter(word: str, letter: str) -> int:
    """
    Count occurrences of a specific letter in a word.
    
    Args:
        word (str): The input word to search in
        letter (str): The specific letter to count
    
    Returns:
        int: The number of occurrences of the letter in the word
    """
    return word.lower().count(letter.lower())

# Create LiteLLM model with LangSmith tracing
litellm_model = LiteLLMModel(
    client_args={
        "api_key": "your-openai-api-key",  # Replace with your actual API key
    },
    model_id="gpt-4o",
    params={
        "temperature": 0.7,
        # LangSmith tracing will be automatically enabled through environment variables
    }
)

# Create agent with LiteLLM model
agent = Agent(
    model=litellm_model,
    tools=[current_time, python_repl, letter_counter],
    system_prompt="You are a helpful assistant that can use tools to answer questions."
)

# Test the agent
message = """
いくつか質問があります。

1. いま日本は何時？
2. その時刻表示の中に「1」はいくつある？
3. ここまで話した内容をPythonコードにして。テストしたあとにコード内容を表示して。
"""

# This will be traced in LangSmith
result = agent(message)
print(result.message)
