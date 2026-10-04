import os

from autogen import ConversableAgent

events = [
    {"timestamp_s": 1500, "signal": "cell_v_min", "value": 3.97, "severity": "high", "note": "cell 37 sagging under load"},
    {"timestamp_s": 3000, "signal": "insulation_kohm", "value": 1200, "severity": "medium", "note": "resistance falling"},
    {"timestamp_s": 4000, "signal": "pack_temp_max_c", "value": 41.5, "severity": "medium"},
    {"timestamp_s": 4750, "signal": "pack_current_a", "value": 12.3, "note": "flat for 70 s"},
    {"timestamp_s": 5500, "signal": "soc_pct", "value": 57.4, "severity": "high", "note": "9 point jump"},
]


def build_events_text(events):
    lines = []
    for e in events:
        severity = e.get("severity", "unknown").upper()
        note = e.get("note", "no note")
        lines.append(f"[{severity}] t={e['timestamp_s']}s | {e['signal']} = {e['value']} | {note}")
    return f"EV FAULT EVENTS ({len(events)} events)\n\n" + "\n".join(lines)


def save_diagnosis_to_txt(diagnosis, transcript, filename="data/diagnosis.txt"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"SUPERVISOR'S VERDICT:\n{diagnosis}\n\n")
        file.write(f"TRANSCRIPT:\n{transcript}\n")


events_text = build_events_text(events)

llm_config = {
    "model": "gemini-3.1-flash-lite",
    "api_type": "google",
    "api_key": os.environ["GEMINI_API_KEY"],
}

battery_analyst = ConversableAgent(
    name="Battery_Analyst",
    llm_config=llm_config,
    human_input_mode="NEVER",
    system_message=(
        "You are a battery engineer with experience in high voltage EV batteries. "
        "You only analyze cell voltage, insulation and temperature events. "
        "Ignore all other signals and do not do the powertrain analyst's job. "
        "Cite the timestamp of every event you mention. Keep replies to 5 sentences."
    ),
)

powertrain_analyst = ConversableAgent(
    name="Powertrain_Analyst",
    llm_config=llm_config,
    human_input_mode="NEVER",
    system_message=(
        "You are a powertrain engineer with experience in battery current, vehicle "
        "speed and SOC. You only analyze current, speed and SOC events. "
        "Ignore all other signals and do not do the battery analyst's job. "
        "Cite the timestamp of every event you mention. Keep replies to 5 sentences."
    ),
)

supervisor = ConversableAgent(
    name="Supervisor",
    llm_config=llm_config,
    human_input_mode="NEVER",
    system_message=(
        "You are a strict supervisor with experience in both powertrains and "
        "batteries. You receive a discussion between a battery analyst and a "
        "powertrain analyst, and you also have the raw events below.\n\n"
        f"{events_text}\n\n"
        "Give a ranked list of likely faults. For each one, cite the timestamps "
        "that support it and say which analyst raised it. Check the analysts' "
        "claims against the raw events. Do not invent causes. If the data does "
        "not support a conclusion, say 'not enough evidence'."
    ),
)

chat_results = battery_analyst.initiate_chat(
    recipient=powertrain_analyst,
    max_turns=3,
    message=(
        "Here are the flagged events:\n\n"
        f"{events_text}\n\n"
        "Powertrain analyst, review only your signals and tell me what is wrong. "
        "I will cover the battery side."
    ),
)

transcript = "\n\n".join(
    f"{m.get('name', m.get('role'))}: {m.get('content')}"
    for m in chat_results.chat_history
)

diagnosis = supervisor.generate_reply(
    messages=[{"role": "user", "content": f"Review this discussion and give the likely diagnosis:\n\n{transcript}"}]
)

# generate_reply may return a dictionary or plain text depending on the version
if isinstance(diagnosis, dict):
    diagnosis = diagnosis.get("content", "")

save_diagnosis_to_txt(diagnosis, transcript)
print(diagnosis)