import os
import logging
from datetime import datetime
from strands import Agent, tool
from strands.models.litellm import LiteLLMModel
from strands_tools import current_time, python_repl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up LangSmith environment variables
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"] = "your-langsmith-api-key"  # Replace with your actual API key
os.environ["LANGCHAIN_PROJECT"] = "strands-agents-advanced"  # Replace with your project name

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

# Custom callback handler for detailed logging and LangSmith integration
class LangSmithCallbackHandler:
    def __init__(self):
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.tool_uses = []
        self.conversation_log = []
    
    def __call__(self, **kwargs):
        timestamp = datetime.now().isoformat()
        
        if "data" in kwargs:
            # Log streaming text data
            text_chunk = kwargs["data"]
            logger.info(f"[{timestamp}] Text chunk: {text_chunk}")
            self.conversation_log.append({
                "type": "text_chunk",
                "timestamp": timestamp,
                "data": text_chunk
            })
        
        elif "current_tool_use" in kwargs:
            # Log tool usage
            tool_info = kwargs["current_tool_use"]
            tool_name = tool_info.get("name", "unknown")
            tool_id = tool_info.get("toolUseId", "unknown")
            
            if tool_id not in [t["id"] for t in self.tool_uses]:
                logger.info(f"[{timestamp}] Tool used: {tool_name} (ID: {tool_id})")
                self.tool_uses.append({
                    "id": tool_id,
                    "name": tool_name,
                    "timestamp": timestamp,
                    "input": tool_info.get("input", {})
                })
        
        elif "tool_result" in kwargs:
            # Log tool results
            tool_result = kwargs["tool_result"]
            logger.info(f"[{timestamp}] Tool result received")
            # You could send this data to LangSmith here
        
        elif "error" in kwargs:
            # Log errors
            error = kwargs["error"]
            logger.error(f"[{timestamp}] Error: {error}")
    
    def get_session_summary(self):
        return {
            "session_id": self.session_id,
            "total_tool_uses": len(self.tool_uses),
            "tools_used": [t["name"] for t in self.tool_uses],
            "conversation_length": len(self.conversation_log)
        }

# Create callback handler instance
callback_handler = LangSmithCallbackHandler()

# Create LiteLLM model
litellm_model = LiteLLMModel(
    client_args={
        "api_key": "your-openai-api-key",  # Replace with your actual API key
    },
    model_id="gpt-4o",
    params={
        "temperature": 0.7,
    }
)

# Create agent with custom callback handler
agent = Agent(
    model=litellm_model,
    tools=[current_time, python_repl, letter_counter],
    system_prompt="You are a helpful assistant that can use tools to answer questions.",
    callback_handler=callback_handler
)

# Test the agent
message = """
いくつか質問があります。

1. いま日本は何時？
2. その時刻表示の中に「1」はいくつある？
3. ここまで話した内容をPythonコードにして。テストしたあとにコード内容を表示して。
"""

print("Starting agent conversation...")
result = agent(message)

print("\n" + "="*50)
print("CONVERSATION COMPLETE")
print("="*50)
print(f"Final response: {result.message}")

# Print session summary
summary = callback_handler.get_session_summary()
print(f"\nSession Summary:")
print(f"- Session ID: {summary['session_id']}")
print(f"- Total tool uses: {summary['total_tool_uses']}")
print(f"- Tools used: {', '.join(summary['tools_used'])}")
print(f"- Conversation length: {summary['conversation_length']} events")
