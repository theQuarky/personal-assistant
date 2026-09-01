# Personal Assistant

A local-first Linux personal assistant that remembers context, manages workload, schedules reminders, and provides an LLM conversational interface.

## Vision

This is not intended to be another chatbot. The assistant separates durable personal state from LLM reasoning:

- SQLite stores tasks, projects, commitments, reminders, and structured memories.
- An LLM interprets natural language and reasons over retrieved context.
- A deterministic workload engine calculates what is realistic.
- A scheduler handles reminders independently of the LLM.
- Conversation importers will ingest ChatGPT, Claude, and Gemini exports.
- The Linux desktop widget provides a fast view of today and upcoming work.

## Planned stack

- Python 3.12+
- FastAPI
- SQLite
- Ollama
- GTK4 / Libadwaita
- systemd user services/timers
- Local embeddings for semantic memory

## Development status

Early bootstrap. V0.1 focuses on the domain model, SQLite persistence, workload calculation, and a small CLI/API foundation before adding the desktop UI and LLM tools.

## Privacy

The design is local-first. No cloud AI provider is required for normal operation. Imported conversations and personal data should remain on the local machine unless the user explicitly configures an external service.
