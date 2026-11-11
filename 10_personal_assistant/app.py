"""Personal assistant that plans your meals and your week, and remembers your preferences.
Usage:  python app.py
Commands inside the chat:
  /meals    -> 7-day meal plan + grocery list
  /week     -> weekly schedule from your tasks and goals
  /remember <fact>   e.g. /remember I'm vegetarian and work 9-6
  /save     -> save the last plan to plan.md
  /quit
"""
import json, os, datetime
import anthropic

MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")
MEMORY_FILE = "memory.json"
client = anthropic.Anthropic()


def load_memory():
    return json.load(open(MEMORY_FILE, encoding="utf-8")) if os.path.exists(MEMORY_FILE) else []


def save_memory(mem):
    json.dump(mem, open(MEMORY_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def system_prompt(memory):
    today = datetime.date.today().strftime("%A, %Y-%m-%d")
    facts = "\n".join(f"- {m}" for m in memory) or "- (nothing yet)"
    return (f"You are a friendly, practical personal assistant. Today is {today}.\n"
            f"What you know about the user:\n{facts}\n\n"
            "Plan meals and weeks that respect these facts. Use clear markdown tables and lists. "
            "Keep meals realistic (prep time, leftovers, budget). For schedules, protect sleep and breaks. "
            "Ask at most one short question if something essential is missing.")


def ask(history, memory):
    reply = client.messages.create(model=MODEL, max_tokens=2000,
                                   system=system_prompt(memory), messages=history[-11:]).content[0].text
    history.append({"role": "assistant", "content": reply})
    return reply


SHORTCUTS = {
    "/meals": "Make me a 7-day meal plan (breakfast, lunch, dinner) as a table, then a grocery list grouped by store section.",
    "/week": "Ask me for this week's tasks and goals if you don't know them, then build a day-by-day schedule for Mon-Sun.",
}


def main():
    memory = load_memory()
    history, last_plan = [], ""
    print("Personal assistant ready. Type /meals, /week, /remember, /save or just chat.")
    while True:
        text = input("\nYou: ").strip()
        if not text:
            continue
        if text == "/quit":
            break
        if text.startswith("/remember"):
            memory.append(text[len("/remember"):].strip())
            save_memory(memory)
            print("Got it, I'll remember that.")
            continue
        if text == "/save":
            with open("plan.md", "w", encoding="utf-8") as f:
                f.write(last_plan or "No plan yet.")
            print("Saved plan.md")
            continue

        history.append({"role": "user", "content": SHORTCUTS.get(text, text)})
        last_plan = ask(history, memory)
        print(f"\nAssistant:\n{last_plan}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nBye!")
