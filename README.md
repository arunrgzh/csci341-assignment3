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
├── DEPLOYMENT.md              # Deployment instructions
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

## 🎯 Features

### Complete CRUD Operations

- **Create**: Add new records to any table
- **Read**: View all records with formatted display
- **Update**: Edit existing records with validation
- **Delete**: Remove records with cascade handling

### Database Tables

1. **User Account** - Base user information
2. **Caregiver** - Caregiver profiles with rates and types
3. **Member** - Member profiles with house rules
4. **Address** - Member addresses
5. **Job** - Job postings by members
6. **Job Application** - Applications from caregivers
7. **Appointment** - Scheduled caregiving sessions

### User Interface

- Responsive design with modern UI
- Dashboard with statistics
- Navigation menu for all tables
- Form validation with error messages
- Confirmation dialogs for deletions
- Status badges and type indicators

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
DATABASE_URL=postgresql://username:password@localhost:5432/caregivers
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

## 📊 Database Schema

The application manages 7 interconnected tables:

- **user_account**: Core user information (email, name, city, phone)
- **caregiver**: Extends user_account (caregiving type, hourly rate, gender)
- **member**: Extends user_account (house rules, dependent description)
- **address**: Member addresses (house number, street, town)
- **job**: Job postings by members (required type, requirements, date)
- **job_application**: Links caregivers to jobs (application date)
- **appointment**: Scheduled sessions (date, time, hours, status)

## 🎨 Architecture

### Separation of Concerns

**app.py** - Application routes and request handling

- Route definitions for CRUD operations
- Request/response handling
- Template rendering
- Error handling

**models.py** - Database models

- SQLAlchemy ORM models
- Relationships and constraints
- Helper methods (display_name, total_cost, etc.)

**forms.py** - Form handling and validation

- Field configurations for each table
- Validation logic
- Data parsing and coercion
- Dropdown choice generators

**config.py** - Application configuration

- Database connection settings
- Secret key management
- Environment-specific settings

**templates/** - HTML templates

- Individual templates for each table
- Generic form template for create/edit
- Base template with shared layout
- Dashboard with statistics

**static/style.css** - Styling

- Responsive design
- Modern UI components
- Color-coded badges
- Form styling

## 🔧 Usage

### Dashboard

- View statistics for all tables
- Quick access to each table's list view

### List Views

- View all records in a table
- Click "Create New" to add records
- Click "Edit" to modify records
- Click "Delete" to remove records (with confirmation)

### Create/Edit Forms

- Fill in required fields (marked with \*)
- Select from dropdowns for foreign keys
- Date/time pickers for temporal fields
- Validation feedback for errors

### Navigation

- Top navigation bar for quick access
- Breadcrumb-style navigation
- Back buttons on forms

## 🌐 Deployment

See `DEPLOYMENT.md` for detailed deployment instructions for:

- PythonAnywhere (Free tier available)
- Heroku
- Other WSGI-compatible platforms

### Quick Deployment Steps

1. **Update database URL** in `config.py` or set `DATABASE_URL` environment variable
2. **Set secret key** via `SECRET_KEY` environment variable
3. **Install dependencies**: `pip install -r requirements.txt`
4. **Run with Gunicorn**: `gunicorn app:app`

## 🔐 Security Notes

- Change the default `SECRET_KEY` in production
- Use environment variables for sensitive data
- Database credentials should not be committed to version control
- Enable HTTPS in production
- Implement authentication/authorization as needed

## 📝 Development Notes

### Adding New Tables

1. Add model to `models.py`
2. Add form configuration to `forms.py`
3. Add table mapping to `app.py` (TABLE_MODELS)
4. Create template in `templates/` (e.g., `new_table.html`)
5. Add navigation link to `base.html`

### Customizing Forms

Edit field configurations in `forms.py`:

- Add/remove fields
- Change field types (text, select, textarea, etc.)
- Add validation rules
- Customize dropdown choices

### Styling

Modify `static/style.css` to customize:

- Colors and themes
- Layout and spacing
- Responsive breakpoints
- Component styles

## 🐛 Troubleshooting

**Database connection errors:**

- Check PostgreSQL is running
- Verify database credentials in `config.py`
- Ensure database exists and tables are created

**Import errors:**

- Activate virtual environment
- Run `pip install -r requirements.txt`

**Template not found:**

- Ensure template name matches table name exactly
- Check `templates/` directory structure

**Foreign key errors:**

- Ensure referenced records exist
- Check cascade delete settings

## 📚 Technologies Used

- **Backend**: Flask 3.0, SQLAlchemy 2.0
- **Database**: PostgreSQL
- **Frontend**: HTML5, CSS3, Jinja2 templates
- **Deployment**: Gunicorn, WSGI-compatible servers

## 👥 Assignment Information

**Course**: CSCI 341 - Database Systems  
**Assignment**: Assignment 3 - Web Application with CRUD Operations  
**Institution**: Nazarbayev University

## 📄 License

This project is created for educational purposes as part of CSCI 341 coursework.
