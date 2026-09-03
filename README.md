# CuraTwin

An AI-powered personal health monitoring and digital twin platform built for the **Alibaba Cloud AI Hackathon Pakistan 2026**.

CuraTwin helps users track physical wellness, mental health, and female health cycles in one place — with an AI stress-prediction model and a guardian system for caregivers.

## Features

- **Wellness Tracking** — log daily vitals, sleep, hydration, and activity
- **Mood Check-ins** — record emotional state with contextual notes
- **Stress Prediction** — ML model (scikit-learn) predicts stress levels from wellness patterns
- **Cycle Tracking** — menstrual cycle logging with phase insights
- **Coping Engine** — AI-generated coping suggestions based on current state
- **Guardian System** — caregivers can monitor dependents with consent-based access
- **Digital Twin** — a holistic AI model of the user's health state
- **JWT Authentication** — secure, token-based user accounts

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python 3.12) |
| Database | Neon Postgres (prod) / SQLite (dev) |
| ORM | SQLAlchemy |
| Auth | JWT (HS256) via python-jose |
| ML | scikit-learn, NumPy, Joblib |
| Frontend | Vanilla JS SPA (hash routing) |
| Hosting | Vercel (serverless Python function) |

## Project Structure

```
curatwin/
├── api/index.py          # Vercel serverless entrypoint
├── backend/
│   ├── config.py         # Environment-based configuration
│   ├── database.py       # SQLAlchemy engine & session
│   ├── main.py           # FastAPI app factory
│   ├── ai/               # ML model & stress prediction
│   ├── middleware/        # JWT auth middleware
│   ├── models/           # SQLAlchemy ORM models
│   ├── routers/          # API route handlers
│   ├── schemas/          # Pydantic request/response schemas
│   └── services/         # Business logic (affective, coping, cycle, etc.)
├── frontend/
│   ├── index.html        # SPA shell
│   ├── css/              # Styles
│   └── js/               # App logic, API client, auth, pages, components
├── tests/                # pytest test suite
├── scripts/              # Database initialization scripts
├── vercel.json           # Vercel deployment config
├── pyproject.toml        # Python project metadata
└── requirements.txt      # Pinned dependencies
```

## Getting Started

### Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/maryamsamee00-ux/CuraTwin.git
   cd CuraTwin/curatwin
   ```

2. Install dependencies:
   ```bash
   uv sync
   # or
   pip install -r requirements.txt
   ```

3. Copy the example environment file and edit it:
   ```bash
   cp .env.example .env
   # Fill in your values in .env
   ```

4. Run locally:
   ```bash
   uv run python run.py
   ```
   The app starts at `http://localhost:8000`. Local dev uses SQLite automatically.

### Running Tests

```bash
uv run pytest
```

## Deployment

The app is deployed to Vercel as a single Python serverless function. See `vercel.json` for the routing config. Environment variables are set via the Vercel dashboard.

## Environment Variables

See [`.env.example`](.env.example) for all available configuration options.

## License

Built for the Alibaba Cloud AI Hackathon Pakistan 2026.
