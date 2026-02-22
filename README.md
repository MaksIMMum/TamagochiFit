# 🥚 TamagochiFit

> *Grow your virtual companion through a healthy lifestyle!*

TamagochiFit is a Tamagotchi-inspired fitness web application where your daily health habits — workouts, nutrition, and activity — directly affect the growth and happiness of your virtual pet. Built with a FastAPI backend, SQLite database, and a pixel-art themed frontend.

---

## ✨ Features

- **User Authentication** — Secure registration and login with JWT access + refresh tokens
- **Virtual Pet System** — Your pet evolves based on your real-world fitness activity
- **Workout Tracking** — Log exercises across muscle groups
- **Nutrition** — Browse healthy recipes and track food intake
- **Social** — Leaderboards and social features to compete with friends

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI 0.129.2 |
| Validation | Pydantic 2.12.5 |
| Database | SQLite + SQLAlchemy 2.0 |
| Migrations | Alembic 1.18.4 |
| Auth | JWT via `python-jose`, bcrypt |
| Frontend | HTML, CSS, Bootstrap 5, Vanilla JS |
| Testing | pytest + requests |

---

## 📁 Project Structure

```
TamagochiFit/
├── app/
│   ├── models/          # SQLAlchemy ORM models (User, Pet, Activity...)
│   ├── routes/          # FastAPI route handlers (auth, pages, character...)
│   ├── schemas/         # Pydantic request/response schemas
│   ├── services/        # Business logic (user_service, security, nutrition_api...)
│   ├── templates/       # HTML templates (login, register, dashboard...)
│   ├── static/          # CSS, JS, images
│   │   ├── css/
│   │   └── js/
│   ├── utils/           # Dependencies (JWT auth middleware)
│   ├── database.py      # SQLAlchemy engine + session setup
│   └── main.py          # FastAPI app entry point
├── alembic/             # Database migrations
│   └── versions/
├── data/                # SQLite database file
├── docs/                # Architecture diagrams
├── tests/               # Integration tests
├── config.py            # App settings (loaded from .env)
├── requirements.txt
└── .env.example
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/MaksIMMum/TamagochiFit.git
   cd TamagochiFit
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv

   # macOS/Linux
   source .venv/bin/activate

   # Windows
   .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and fill in your values:
   ```env
   APP_NAME=TamagochiFit
   DEBUG=True
   DATABASE_URL=sqlite:///./TamagochiFit.db
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   fastapi dev app/main.py
   ```

The app will be available at **http://localhost:8000**. API docs are at **http://localhost:8000/docs**.

---

## 🔑 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register` | Register a new user |
| `POST` | `/api/auth/login` | Login and receive JWT tokens |
| `POST` | `/api/auth/refresh` | Refresh access token |
| `GET` | `/api/auth/me` | Get current user info |
| `POST` | `/api/auth/logout` | Logout (client-side token deletion) |
| `GET` | `/login` | Login page |
| `GET` | `/register` | Registration page |
| `GET` | `/dashboard` | Dashboard (requires auth) |
| `GET` | `/health` | Health check |

---

## 🗄️ Database Migrations

```bash
# Create a new migration after changing models
alembic revision --autogenerate -m "Description of change"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# Check current version
alembic current
```

---

## 🧪 Testing

Run the manual integration test suite (requires the server to be running):

```bash
python tests/test_auth.py
```

For unit tests with pytest:
```bash
pytest
```

---

## ☁️ Deployment

### Deploy to FastAPI Cloud

```bash
fastapi login
fastapi deploy
```

Your app will be live at `https://myapp.fastapicloud.dev`.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue to discuss your idea before submitting a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

**Status:** 🚧 In Development
