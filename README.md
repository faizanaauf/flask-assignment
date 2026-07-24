# Personal Library Tracker

A Flask CRUD application for tracking books in a personal library.

## Features
- Book model with title, author, genre, status, rating, published year, and notes
- App Factory pattern with `create_app()` in `library_tracker/app/__init__.py`
- Two blueprints: HTML `main` and JSON API `api`
- SQLite database with Flask-SQLAlchemy
- Genre filter persisted in session
- PRG pattern for create/edit/delete
- Custom 404 and 500 error pages
- Bootstrap 5 styling

## Setup

1. Open a terminal in `library_tracker`.
2. Create a virtual environment:

```powershell
python -m venv venv
```

3. Activate the virtual environment:

```powershell
venv\Scripts\Activate.ps1
```

4. Install dependencies:

```powershell
pip install -r requirements.txt
```

5. Run the app:

```powershell
python run.py
```

6. Open `http://127.0.0.1:5000` in your browser.

## API Endpoints

- `GET /api/books`
- `GET /api/books/<id>`
- `POST /api/books`
- `PUT /api/books/<id>`
- `DELETE /api/books/<id>`

## Notes

- The default database file is `library_tracker.db`
- To use test config, set `FLASK_CONFIG=TestConfig` and call `create_app(TestConfig)` manually
