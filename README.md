# Stang

> A 3-layer agentic architecture for reliable, deterministic task execution.

## Architecture

This project follows a strict 3-layer separation of concerns (see `CLAUDE.md` for full details):

| Layer | Location | Purpose |
|---|---|---|
| **Directive** | `directives/` | Markdown SOPs — *what* to do |
| **Orchestration** | Agent (LLM) | Intelligent routing & decision-making |
| **Execution** | `execution/` | Deterministic Python scripts — *doing* the work |

## Directory Structure

```
Stang/
├── directives/       # Markdown SOPs (living documents)
├── execution/        # Python utility scripts
├── frontend/         # Next.js app (when applicable)
├── backend/          # FastAPI backend (when applicable)
├── .tmp/             # Intermediate processing files (never committed)
├── .env              # Secrets (never committed — see .env.example)
├── .env.example      # Template for required environment variables
├── .gitignore
├── CLAUDE.md         # Agent instructions & operating principles
└── README.md
```

## Getting Started

1. **Clone the repo**
2. **Copy `.env.example` to `.env`** and fill in your values
3. **Install Python dependencies** (per script — see `execution/requirements.txt` if present)
4. **Install frontend dependencies** (if using the web app):
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Key Principles

- `.tmp/` files are always regenerable — can be deleted freely
- Directives are updated as the agent learns (API limits, edge cases, etc.)
- Deliverables live in cloud services (Google Sheets, Firebase, etc.)
- Business logic lives in `execution/` scripts, not in the agent
