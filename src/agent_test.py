import os

from autogen import ConversableAgent

llm_config = {
    "model": "gemini-3.1-flash-lite",
    "api_type": "google",
    "api_key": os.environ["GEMINI_API_KEY"],
}

agent = ConversableAgent(
    name="fun_fact_agent",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

reply = agent.generate_reply(
    messages=[{"role": "user", "content": "Tell me a fun fact about money"}]
)

print(reply)