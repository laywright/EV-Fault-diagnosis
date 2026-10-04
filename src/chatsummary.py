import os
from google import genai
from autogen import ConversableAgent
llm_config = {
    "model": "gemini-3.1-flash-lite",
    "api_type": "google",
    "api_key": os.environ["GEMINI_API_KEY"],
}
alex = ConversableAgent(
    name = "Alex",
    llm_config=llm_config,
    system_message= "Your name is Alex and you are a AI specialist"
)
sam = ConversableAgent(
    name = "Sam",
    llm_config=llm_config,
    system_message= "Your name is Alex and you are a AI specialist"
)
chat_results=alex.initiate_chat(
    recepient=sam,
    max_turns=3,
    summary_method="Reflection with llm",
    summary_prompt= "Summarize the conversation"
)