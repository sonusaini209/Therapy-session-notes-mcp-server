# 🧠 Therapist Session Notes — MCP Server

An MCP (Model Context Protocol) server for managing therapy session notes. Built with [FastMCP](https://github.com/jlowin/fastmcp), it allows AI assistants like Claude to save, retrieve, and analyze patient session data through a simple set of tools.

---

## Features

- 📝 Save therapy session notes with themes and sentiment scores
- 📈 Track patient sentiment trends over time
- 🔍 Retrieve sessions by patient name or specific date
- 🗂️ Identify recurring themes across a patient's history
- 🗑️ Delete all data for a patient

---

## Tech Stack

- **Python 3.10+**
- **FastMCP** — MCP server framework
- **SQLite** — Local database (`sessions.db`)

---

## Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd therapist-session-notes
   ```

2. **Install dependencies**
   ```bash
   pip install fastmcp
   ```

3. **Run the server**
   ```bash
   python server.py
   ```

---

## Available MCP Tools

| Tool | Description |
|---|---|
| `save_session` | Save a session with notes, themes, and a sentiment score |
| `get_recent_sessions` | Fetch the most recent N sessions for a patient |
| `get_sentiment_trend` | Get sentiment scores over time for a patient |
| `get_all_themes` | List all themes across a patient's session history |
| `get_session_by_date` | Retrieve a specific session by date (`YYYY-MM-DD`) |
| `delete_patient_data` | Delete all session records for a patient |

---

## Data Model

Each session record stores:

| Field | Type | Description |
|---|---|---|
| `patient_name` | `TEXT` | Name of the patient |
| `date` | `TEXT` | Session date (`YYYY-MM-DD`) |
| `notes` | `TEXT` | Free-form session notes |
| `themes` | `TEXT` (JSON) | Key topics, e.g. `["grief", "sleep"]` |
| `sentiment_score` | `REAL` | Float from `-1.0` (crisis) to `1.0` (thriving) |

---

## Usage Example

When connected to an AI assistant via MCP, you can prompt it naturally:

> *"Save a session for John Doe today. He discussed work stress and sleep issues. Sentiment was mildly positive."*

> *"Show me the sentiment trend for Jane Smith over her last 10 sessions."*

---

## Notes

- The SQLite database (`sessions.db`) is auto-created in the same directory as the script on first run.
- Patient data is stored locally and never leaves your machine.

---

## License

MIT
