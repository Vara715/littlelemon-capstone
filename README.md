# Little Lemon Web Application (Meta Back-End Developer Capstone)

Django + Django REST Framework backend with MySQL, Djoser token authentication, a static home page, and unit tests.

## Project structure
```
littlelemon/                 <- repo root
├── manage.py
├── requirements.txt
├── Readme.txt / README.md
├── littlelemon/             <- project package (settings.py, urls.py, wsgi.py, asgi.py)
├── restaurant/              <- app (models, serializers, views, urls, tests, templates)
│   ├── migrations/0001_initial.py
│   ├── templates/index.html
│   └── tests/test_models.py, test_views.py
└── static/                  <- css/style.css, js/main.js, img/logo.svg
```

## Setup
1. Create and activate a virtualenv
   - macOS/Linux: `python3 -m venv venv && source venv/bin/activate`
   - Windows: `python -m venv venv && venv\Scripts\activate`
2. Install dependencies: `pip install -r requirements.txt`
   (mysqlclient needs MySQL client libs: Ubuntu `sudo apt install default-libmysqlclient-dev build-essential pkg-config`; macOS `brew install mysql pkg-config`)
3. Create the database in MySQL: `CREATE DATABASE littlelemon CHARACTER SET utf8mb4;`
4. Set credentials. `settings.py` reads `DB_USER`, `DB_PASSWORD`, `DB_HOST` (default 127.0.0.1), `DB_PORT` (default 3306), `DB_NAME` (default littlelemon). Either export them or edit the defaults in `littlelemon/settings.py`.
   - e.g. `export DB_USER=root DB_PASSWORD=yourpassword`
5. Migrate: `python manage.py makemigrations && python manage.py migrate`
6. (Optional) admin user: `python manage.py createsuperuser`
7. Run: `python manage.py runserver` then open http://127.0.0.1:8000/
8. Tests: `python manage.py test` (needs MySQL permission to create `test_littlelemon`; for a quick check without MySQL use `USE_SQLITE=1 python manage.py test`)

## API endpoints
| Method | URL | Auth | Purpose |
|---|---|---|---|
| GET | `/` | none | Home page (static assets) |
| GET / POST | `/restaurant/menu/` | GET public, POST needs token | List / create menu items |
| GET / PUT / PATCH / DELETE | `/restaurant/menu/<id>` | GET public, others need token | Single menu item |
| GET / POST | `/restaurant/booking/tables/` | **Token required** | List / create bookings |
| GET / PUT / PATCH / DELETE | `/restaurant/booking/tables/<id>/` | **Token required** | Single booking |
| POST | `/auth/users/` | none | Register a user |
| GET | `/auth/users/me/` | token | Current user |
| POST | `/auth/token/login/` | none | Obtain token |
| POST | `/auth/token/logout/` | token | Revoke token |
| GET | `/admin/` | superuser | Django admin |

## Insomnia / Postman testing steps
1. **Register**: POST `/auth/users/` JSON `{"username":"lemonuser","password":"StrongPass123!","email":"a@b.com"}` -> 201.
2. **Login**: POST `/auth/token/login/` JSON `{"username":"lemonuser","password":"StrongPass123!"}` -> `{"auth_token":"<token>"}`.
3. **Menu (public)**: GET `/restaurant/menu/` -> 200 (no header needed).
4. **Create menu item**: POST `/restaurant/menu/` with header `Authorization: Token <token>`, body `{"title":"Greek Salad","price":"12.50","inventory":20}` -> 201.
5. **Single item**: GET `/restaurant/menu/1`; PUT/PATCH to update; DELETE to remove.
6. **Bookings without token**: GET `/restaurant/booking/tables/` -> 401.
7. **Bookings with token**: add header `Authorization: Token <token>`; POST `{"name":"Alice","no_of_guests":4,"booking_date":"2026-12-01T19:00:00Z"}` -> 201; GET list -> 200.
8. **Logout**: POST `/auth/token/logout/` with the token header -> 204.

## Suggested git commit milestones
1. `chore: initial Django project, .gitignore and requirements.txt`
2. `feat: create restaurant app and configure MySQL + static files`
3. `feat: add MenuItem and Booking models with migrations`
4. `feat: add serializers and DRF views for menu and bookings`
5. `feat: configure URL routes and DefaultRouter for bookings`
6. `feat: integrate Djoser and token authentication`
7. `feat: add static index.html, CSS and JS`
8. `test: add model and view unit tests`
9. `docs: add Readme.txt and README.md`
