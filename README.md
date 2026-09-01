# Personal Assistant MVP

A local-first Linux assistant for remembering work, tracking tasks, and showing workload.

## Quick start

```bash
git clone https://github.com/theQuarky/personal-assistant.git
cd personal-assistant
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Add work:

```bash
pa add "Finish cybersecurity report" --due "2026-09-04 18:00" --minutes 120 --priority 5
pa add "Read research paper" --minutes 60 --priority 3
pa today
```

Launch the desktop view:

```bash
python -m assistant.widget
```

Launch the API:

```bash
uvicorn assistant.api:app --reload
```

The local database lives at `~/.local/share/personal-assistant/assistant.db`.

## Roadmap

- Natural-language task creation with Ollama
- Persistent semantic memory
- ChatGPT / Claude / Gemini importers
- Workload-aware scheduling
- Linux notifications and systemd reminders
- GTK4/Libadwaita desktop widget
