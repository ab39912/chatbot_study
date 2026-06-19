# Discourse Assessment — Voice Chatbot (Streamlit)

Voice-only chatbot for administering Section I (First Encounter) of the discourse assessment protocol.

## Setup

Install the single dependency:
```bash
pip install streamlit
```

## API Key

Three ways to provide your Anthropic API key (in order of preference):

**Option A — Streamlit secrets (recommended for deployment)**
Create `.streamlit/secrets.toml` next to `app.py`:
```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

**Option B — Environment variable**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
streamlit run app.py
```

**Option C — Sidebar input**
Leave the above unset and paste the key into the sidebar when the app loads.

## Run

```bash
streamlit run app.py
```

Then open http://localhost:8501 in **Chrome or Edge** (required for Web Speech API).

## Protocol Notes

- The AI partner delivers the protocol opening and then listens automatically
- Participant speech is detected via the browser's built-in speech recognition
- After ~2.5 seconds of silence, the AI processes the turn and responds aloud
- Session ends automatically at 5 minutes, or manually via "End Session"
- The italic pill at the bottom shows live speech capture (for the examiner to monitor)

## Security Note

This app injects the API key server-side into the embedded HTML component.
It is intended for **local or controlled internal use** — not public deployment without additional authentication.
