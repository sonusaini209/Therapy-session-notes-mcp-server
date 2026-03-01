#  Therapy Session Notes MCP Server

An MCP (Model Context Protocol) server for managing therapy session notes. Built with [FastMCP](https://github.com/jlowin/fastmcp), it allows AI assistants like Claude to save, retrieve, and analyze patient session data through a simple set of tools.

---

## Features

-  Save therapy session notes with themes and sentiment scores
-  Track patient sentiment trends over time
-  Retrieve sessions by patient name or specific date
-  Identify recurring themes across a patient's history
-  Delete all data for a patient

---

## Tech Stack

- **Python 3.10+**
- **FastMCP** — MCP server framework
- **SQLite** — Local database (`sessions.db`)

---

## Installation

### Prerequisites

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/) — fast Python package manager

Install `uv` if you don't have it:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/SonuSaini/therapy-session-notes-mcp-server
   cd therapy-session-notes-mcp-server
   ```
   Then open it in VS Code:
   ```bash
   code .
   ```

   > This gives you `main.py` with all the MCP tools already written.

2. **Initialize the project with uv**
   ```bash
   uv init .
   ```

3. **Install FastMCP**
   ```bash
   uv add fastmcp
   ```

4. **Verify FastMCP is installed**
   ```bash
   uv run fastmcp version
   ```

5. **Test the server**
   ```bash
   uv run fastmcp dev main.py
   ```

6. **Run the server**
   ```bash
   uv run fastmcp run main.py
   ```

---

## Connecting to Claude Desktop

The easiest way is using the `fastmcp install` command — it automatically registers the server in your Claude Desktop config:

```bash
uv run fastmcp install main.py
```

Restart Claude Desktop and you'll see the 🔨 tools icon in the chat input confirming it's connected.


---

## Usage Examples

Once connected, talk to Claude naturally:

> *"Save a session for John Doe today. He talked about work stress and trouble sleeping. Sentiment was mildly positive."*

> *"What themes has Jane Smith been discussing over the last month?"*

> *"Show me the sentiment trend for John Doe."*

> *"Get Jane's session from 2025-06-15."*

> *"Delete all data for John Doe."*

Claude will automatically call the right tools behind the scenes.

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
| `themes` | `TEXT` (JSON) | Key topics, e.g. `["grief", "sleep", "work stress"]` |
| `sentiment_score` | `REAL` | Float from `-1.0` (crisis) to `1.0` (thriving) |

---

## Notes

- The SQLite database (`sessions.db`) is auto-created in the same directory as `main.py` on first run.
- All patient data is stored locally and never leaves your machine.

---

## License

MIT — see [LICENSE](./LICENSE) for details.
