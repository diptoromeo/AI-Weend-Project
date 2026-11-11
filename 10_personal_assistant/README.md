# 10 · Personal Assistant

A chat assistant that plans your meals and your week. It remembers facts about you (diet, work hours, goals) between sessions and can save plans to a file.

## Setup
```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...
```

## Run
```bash
python app.py
```

## Commands
| Command | What it does |
|---------|--------------|
| `/remember <fact>` | Saves a fact, e.g. `/remember I'm vegetarian and work 9-6` |
| `/meals` | 7-day meal plan table + grocery list by store section |
| `/week` | Day-by-day schedule from your tasks and goals |
| `/save` | Saves the last plan to `plan.md` |
| `/quit` | Exit |

You can also chat normally: "Swap Wednesday dinner for something under 20 minutes."

## Example
```
You: /remember I'm vegetarian, budget 70,000 won a week
Got it, I'll remember that.

You: /meals
Assistant:
| Day | Breakfast | Lunch | Dinner |
| Mon | Overnight oats | Tofu bibimbap | Vegetable curry |
...
```

## Files it creates
- `memory.json`: your saved facts (edit or delete it to reset).
- `plan.md`: the last plan you saved.

## Ideas to extend
- Export the weekly schedule to Google Calendar.
- Add a Streamlit UI with a checklist for the grocery list.
