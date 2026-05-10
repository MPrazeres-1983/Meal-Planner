# Meal Planner 🍽️

![CI/CD Pipeline](https://github.com/MPrazeres-1983/Meal-Planner/actions/workflows/tests.yml/badge.svg)
![Codecov](https://codecov.io/gh/MPrazeres-1983/Meal-Planner/branch/main/graph/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.13+-blue.svg)

**Meal Planner** is a full-stack web application for recipe management and weekly meal planning, developed as the final project of the Computer Engineering degree at Universidade Aberta.

The project received a final grade of **19/20** and focuses on user authentication, role-based access control, recipe workflows, weekly planning, administration features and automated testing.

---

## 🚀 Live Demo

- **Online version:** [https://meal-planner-8zsa.onrender.com](https://meal-planner-8zsa.onrender.com)
- **Official repository:** [https://github.com/MPrazeres-1983/Meal-Planner](https://github.com/MPrazeres-1983/Meal-Planner)

> The application is hosted on Render. If the service has been idle, the first request may take a few seconds to wake up.

---

## 📋 Main Features

### User Features

- User registration and authentication.
- Recipe search with filters.
- Public and private recipe submission.
- Weekly meal planning for breakfast, lunch and dinner.
- Create, edit, view and delete weekly meal plans.
- Favourite recipes.
- Blocked recipes.
- PDF export for meal plans, available locally.

### Administration Features

- Approve or reject submitted recipes.
- Manage users.
- Block users.
- Edit user data.
- Change user role or level.
- Delete users.
- Manage recipe categories.
- Create, edit and delete categories.

### User Roles

- Standard user.
- Premium user.
- Administrator.

---

## 🛠️ Tech Stack

| Area | Technology |
| ---- | ---------- |
| Backend | Python, Flask |
| Frontend | HTML, CSS, Jinja2 |
| Database | PostgreSQL in production, SQLite for local/test usage |
| ORM | SQLAlchemy |
| Forms | WTForms |
| Security | Werkzeug password hashing |
| Testing | pytest |
| CI/CD | GitHub Actions |
| Coverage | Codecov |
| Deployment | Render |
| Version Control | Git, GitHub |

---

## 🏗️ Project Structure

```text
Meal-Planner/
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── models/
│   ├── forms/
│   ├── routes/
│   ├── services/
│   ├── static/
│   └── templates/
├── docs/
│   └── Relatorio_Final_MealPlanner.pdf
├── instance/
├── requirements.txt
├── config.py
├── run.py
├── Procfile
├── .gitignore
└── README.md
```

---

## ⚙️ Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/MPrazeres-1983/Meal-Planner.git
cd Meal-Planner
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Linux/macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the repository root.

```env
FLASK_ENV=development
DATABASE_URL=postgresql://<user>:<password>@<host>:<port>/<database>
SECRET_KEY=change-this-secret-locally
```

For a simple local setup, you can adapt the configuration to use SQLite.

### 5. Run the application

```bash
flask run
```

The application should be available at:

```text
http://127.0.0.1:5000
```

---

## 🧪 Testing & Quality

The project includes **31 automated tests** built with `pytest`.

The test suite validates the main functional and security-related areas of the application.

| Area | Tests | Main Validation Points |
| ---- | ----: | ---------------------- |
| Authentication | 8 | Registration flow, password hashing and session persistence |
| Recipe Management | 10 | CRUD operations, image upload and search filters |
| Meal Plans | 7 | Weekly planning logic, date validation and referential integrity |
| Administration | 6 | Role-based access control, user management and content approval |

### Testing Infrastructure

- **Framework:** pytest.
- **HTTP simulation:** Flask test client.
- **Isolation:** SQLite in-memory database for fast and repeatable tests.
- **CI:** GitHub Actions.
- **Coverage:** Codecov.

### Run tests locally

```bash
pytest -v
```

Run tests with coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

---

## 🔐 Quality and Security Focus

This project includes several quality and security concerns relevant to real-world web applications:

- Authentication and session handling.
- Password hashing.
- Role-based access control.
- Admin-only routes.
- User-generated content approval.
- Data validation through forms.
- Separation of routes, models, forms and services.
- Automated regression checks through the test suite.

---

## 📖 Documentation and Final Report

The complete academic report includes the project context, requirements, entity-relationship diagrams, data models, implementation details and user manual.

👉 [View Final Report PDF](./docs/Relatorio_Final_MealPlanner.pdf)

---

## 👥 Authors

| Name | GitHub |
| ---- | ------ |
| **Mário Prazeres** | [@MPrazeres-1983](https://github.com/MPrazeres-1983) |
| **Matilde Carmo** | [@luniballony](https://github.com/luniballony) |

Special thanks to Professor Pedro Pestana for the guidance and feedback throughout the project.

---

## 📬 Contact and Support

For suggestions, bugs or technical questions:

- [Open an issue](https://github.com/MPrazeres-1983/Meal-Planner/issues)
- Contact Mário Prazeres through GitHub or LinkedIn.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
