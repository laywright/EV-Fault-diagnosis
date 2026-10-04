import os 
from autogen import ConversableAgent

llm_config = {
    "model": "gemini-3.1-flash-lite",
    "api_type": "google",
    "api_key": os.environ["GEMINI_API_KEY"],
}
alex = ConversableAgent(
    name = "Alex",
    llm_config=llm_config,
    human_input_mode="NEVER",
    system_message= "Your name is Alex and you are a comedian in a 2 personcomedy give 3 jokes about coding",
    
)
sam =ConversableAgent(
    name="Sam",
    llm_config=llm_config,
    human_input_mode="NEVER",
    system_message= "Your name is Sam and you are a comedian reply with banter to the jokes mentioned"
)
chat_results= alex.initiate_chat(
    recipient = sam,
    message= "Alex tell me a joke",
    max_turns=3
    
)
import pprint
pprint.pprint(chat_results.chat_history)
pprint.pprint(chat_results.cost)