# Caregiver Management System - CRUD Web Application

A full-stack web application for managing a caregiver database with complete CRUD (Create, Read, Update, Delete) functionality.

## 📁 Project Structure

```
csci341-assignment3/
├── app.py                      # Main Flask application with routes
├── models.py                   # Database models (SQLAlchemy)
├── forms.py                    # Form configurations and validation
├── config.py                   # Application configuration
├── requirements.txt            # Python dependencies
├── Procfile                    # Deployment configuration (Heroku/PythonAnywhere)
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navigation
│   ├── index.html             # Dashboard homepage
│   ├── form.html              # Generic form template (create/edit)
│   ├── user_account.html      # Users list view
│   ├── caregiver.html         # Caregivers list view
│   ├── member.html            # Members list view
│   ├── address.html           # Addresses list view
│   ├── job.html               # Jobs list view
│   ├── job_application.html   # Job applications list view
│   └── appointment.html       # Appointments list view
├── static/
│   └── style.css              # Application styles
├── create_tables.sql          # Database schema
├── insert_data.sql            # Sample data
└── queries.py                 # Database queries (from previous assignment)
```


## 🚀 Installation & Setup

### Prerequisites

- Python 3.8+
- PostgreSQL database
- pip (Python package manager)

### Local Development

1. **Clone or navigate to the project directory**

```bash
cd csci341-assignment3
```

2. **Create virtual environment**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up database**

```bash
# Create PostgreSQL database
createdb caregivers

# Run schema
psql -d caregivers -f create_tables.sql

# Insert sample data
psql -d caregivers -f insert_data.sql
```

5. **Configure environment variables**

Create a `.env` file (optional):

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/caregivers
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
```

Or update `config.py` directly with your database credentials.

6. **Run the application**

```bash
# Development mode
python app.py

# Or using Flask CLI
flask --app app run

# Production mode with Gunicorn
gunicorn app:app
```

7. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`



## 👥 Assignment Information

**Course**: CSCI 341 - Database Systems  
**Assignment**: Assignment 3 - Web Application with CRUD Operations  
**Institution**: Nazarbayev University

## 📄 License

This project is created for educational purposes as part of CSCI 341 coursework.
