import os

from autogen import ConversableAgent

llm_config = {
    "model": "gemini-3.1-flash-lite",
    "api_type": "google",
    "api_key": os.environ["GEMINI_API_KEY"],
}

TOPIC = "Does life have meaning if no higher authority judges it?"

dostoevsky = ConversableAgent(
    name="Dostoevsky",
    llm_config=llm_config,
    human_input_mode="NEVER",
    system_message=(
        "You are a philosopher in the spirit of Fyodor Dostoevsky. "
        f"Debate Kafka on this topic: {TOPIC} "
        "Your position: meaning comes through suffering, conscience and moral responsibility. "
        "Answer Kafka's last point directly, then add one new argument. "
        "Keep each reply to 3 to 5 sentences. "
        "When you have made your final point, end with 'I will see you soon'."
    ),
    is_termination_msg=lambda msg: "I will see you soon" in (msg.get("content") or ""),
)

kafka = ConversableAgent(
    name="Kafka",
    llm_config=llm_config,
    human_input_mode="NEVER",
    system_message=(
        "You are a philosopher in the spirit of Franz Kafka. "
        f"Debate Dostoevsky on this topic: {TOPIC} "
        "Your position: the authority that could give life meaning is distant or "
        "unreachable, so meaning cannot be assumed. "
        "Answer Dostoevsky's last point directly, then add one new argument. "
        "Keep each reply to 3 to 5 sentences."
    ),
)

judge = ConversableAgent(
    name="Judge",
    llm_config=llm_config,
    human_input_mode="NEVER",
    system_message=(
        "You are a strict debate judge. You will receive a debate transcript. "
        "Score each speaker from 1 to 10 on: argument strength, responding to "
        "the opponent, and originality. Then name a winner and justify it in "
        "two sentences. Use this exact format:\n"
        "Dostoevsky: strength=_, response=_, originality=_\n"
        "Kafka: strength=_, response=_, originality=_\n"
        "Winner: _\n"
        "Reason: _"
    ),
)

# Round 1: the debate
chat_results = dostoevsky.initiate_chat(
    recipient=kafka,
    max_turns=5,
    message="Kafka, if no one is watching and no one will judge us, why should suffering mean anything?",
)

# Round 2: turn the history into text and hand it to the judge
transcript = "\n\n".join(
    f"{m.get('name', m.get('role'))}: {m.get('content')}"
    for m in chat_results.chat_history
)

verdict = judge.generate_reply(
    messages=[{"role": "user", "content": f"Judge this debate:\n\n{transcript}"}]
)

print("\n===== VERDICT =====")
print(verdict)