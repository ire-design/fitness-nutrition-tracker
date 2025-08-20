# fitness-nutrition-tracker
# Fitness Nutrition Tracker

A modern Python application for tracking fitness, workouts, and nutrition plans for multiple clients.  
Includes both a command line tool and a RESTful API for easy use and integration.

---

## Features

- **Client Management:** Add, list, and manage fitness clients
- **Workout Logging:** Record workouts with exercise, duration, calories burned
- **Nutrition Tracking:** Log meals, calories, macros, notes
- **Analytics:** Get total calories burned and consumed per client
- **CLI Interface:** Interactive command line tool for all features
- **REST API:** Flask-based API for integration with other apps
- **Tabular Reports:** Beautiful tables and colored output for clarity

---

## 🗂️ Project Structure

```
├── app.py              # CLI entrypoint
├── api.py              # REST API server
├── cli.py              # CLI logic
├── config.py           # App configuration
├── db.py               # Database init and session
├── models.py           # SQLAlchemy ORM models
├── requirements.txt    # Python dependencies
├── README.md           # This file
├── .gitignore          # Ignore venv & DB
└── fitness_tracker.db  # SQLite DB (created at runtime)
```

---

## ⚡ Quickstart

### 1. Clone and Setup

```bash
git clone https://github.com/ire-design/fitness-nutrition-tracker.git
cd fitness-nutrition-tracker
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Initialize the Database

```bash
python app.py init
```

---

## CLI Usage

- **Add a client:**  
  `python app.py add-client`
- **List clients:**  
  `python app.py list-clients`
- **Add workout:**  
  `python app.py add-workout`
- **List workouts:**  
  `python app.py list-workouts --client-id <id>`
- **Add nutrition:**  
  `python app.py add-nutrition`
- **List nutrition:**  
  `python app.py list-nutrition --client-id <id>`
- **Analytics:**  
  `python app.py analytics --client-id <id>`

Type `python app.py --help` to see all commands.

---

## API Usage

1. **Start the API server:**
   ```bash
   python api.py
   ```

2. **Example endpoints:**
   - `GET /clients` — list all clients
   - `POST /clients` — add a new client
   - `GET /clients/<id>/workouts` — all workouts for a client
   - `POST /clients/<id>/workouts` — log workout for client
   - `GET /clients/<id>/nutrition` — all nutrition plans for a client
   - `POST /clients/<id>/nutrition` — log nutrition for client
   - `GET /clients/<id>/analytics` — calories summary

_API is Flask-based and returns JSON._

---

## ⚙️ Technologies Used

- Python 3.8+
- Flask
- SQLAlchemy
- Click
- Colorama
- Tabulate

---

## Contributing

Pull requests and suggestions are welcome!  
- Fork the repository
- Create your feature branch
- Commit your changes
- Open a PR

For major changes, please open an issue first to discuss.

---

## License

MIT License

---

**Developed by [@ire-design](https://github.com/ire-design)**  
**[Linked-In](https://www.linkedin.com/in/irene-musau/)**  

