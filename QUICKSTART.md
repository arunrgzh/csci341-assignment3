# Quick Start Guide

Get your Caregiver Management System running in 5 minutes!

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### 2. Configure Database
Edit `config.py` and update the database URL:
```python
SQLALCHEMY_DATABASE_URI = "postgresql://YOUR_USER:YOUR_PASSWORD@localhost:5432/caregivers"
```

### 3. Set Up Database
```bash
# Create database
createdb caregivers

# Or using psql
psql -U postgres
CREATE DATABASE caregivers;
\q

# Run schema
psql -U postgres -d caregivers -f create_tables.sql

# Insert sample data
psql -U postgres -d caregivers -f insert_data.sql
```

### 4. Run Application
```bash
python app.py
```

### 5. Open Browser
Navigate to: **http://localhost:5000**

## 📁 Project Architecture

```
csci341-assignment3/
│
├── 🐍 Python Files
│   ├── app.py          # Flask routes and application logic
│   ├── models.py       # Database models (SQLAlchemy ORM)
│   ├── forms.py        # Form configurations and validation
│   └── config.py       # Application configuration
│
├── 🎨 Frontend
│   ├── templates/      # HTML templates (Jinja2)
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── form.html
│   │   ├── user_account.html
│   │   ├── caregiver.html
│   │   ├── member.html
│   │   ├── address.html
│   │   ├── job.html
│   │   ├── job_application.html
│   │   └── appointment.html
│   └── static/
│       └── style.css   # Application styles
│
├── 🗄️ Database
│   ├── create_tables.sql    # Database schema
│   └── insert_data.sql      # Sample data
│
├── 📦 Configuration
│   ├── requirements.txt     # Python dependencies
│   ├── Procfile            # Deployment config
│   ├── .gitignore          # Git ignore rules
│   ├── README.md           # Full documentation
│   ├── DEPLOYMENT.md       # Deployment guide
│   └── QUICKSTART.md       # This file
│
└── 📊 Legacy
    └── queries.py          # Database queries (Assignment 2)
```

## 🎯 Features Overview

### CRUD Operations
- ✅ **Create** - Add new records with validation
- ✅ **Read** - View all records in formatted tables
- ✅ **Update** - Edit existing records
- ✅ **Delete** - Remove records with confirmation

### Tables Managed
1. **Users** - Base user accounts
2. **Caregivers** - Caregiver profiles
3. **Members** - Member profiles
4. **Addresses** - Member addresses
5. **Jobs** - Job postings
6. **Job Applications** - Applications to jobs
7. **Appointments** - Scheduled sessions

## 🔧 Common Tasks

### Add New Record
1. Navigate to table list page
2. Click "Create New [Table]" button
3. Fill in the form
4. Click "Create" button

### Edit Record
1. Navigate to table list page
2. Click "Edit" button on desired record
3. Modify fields
4. Click "Update" button

### Delete Record
1. Navigate to table list page
2. Click "Delete" button on desired record
3. Confirm deletion in popup

### View Dashboard
- Go to homepage (/)
- See statistics for all tables
- Click on any card to view that table

## 🐛 Troubleshooting

### "Module not found" error
```bash
# Make sure virtual environment is activated
# Windows
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### "Database connection error"
1. Check PostgreSQL is running
2. Verify credentials in `config.py`
3. Ensure database exists: `createdb caregivers`

### "Template not found"
- Ensure all templates are in `templates/` folder
- Check template names match table names exactly

### Port already in use
```bash
# Use a different port
flask run --port 5001

# Or kill the process using port 5000
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9
```

## 📝 Development Workflow

### 1. Make Changes
Edit files in your IDE:
- Routes: `app.py`
- Models: `models.py`
- Forms: `forms.py`
- Templates: `templates/*.html`
- Styles: `static/style.css`

### 2. Test Locally
```bash
python app.py
# Visit http://localhost:5000
```

### 3. Check for Errors
- Watch terminal for error messages
- Check browser console (F12)
- Review Flask debug output

### 4. Commit Changes
```bash
git add .
git commit -m "Description of changes"
```

### 5. Deploy
See `DEPLOYMENT.md` for deployment instructions.

## 🎓 Learning Resources

### Flask
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)

### SQLAlchemy
- [SQLAlchemy ORM Tutorial](https://docs.sqlalchemy.org/en/20/orm/tutorial.html)
- [Flask-SQLAlchemy Docs](https://flask-sqlalchemy.palletsprojects.com/)

### Jinja2 Templates
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
- [Template Designer Docs](https://jinja.palletsprojects.com/en/3.1.x/templates/)

### PostgreSQL
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [psql Commands](https://www.postgresql.org/docs/current/app-psql.html)

## 💡 Tips

1. **Use Virtual Environment** - Always activate venv before working
2. **Check Logs** - Terminal output shows helpful error messages
3. **Test Changes** - Test locally before deploying
4. **Backup Database** - Regular backups prevent data loss
5. **Read Error Messages** - They usually tell you exactly what's wrong

## 🎉 Next Steps

1. ✅ Get application running locally
2. ✅ Explore all CRUD operations
3. ✅ Customize styling in `style.css`
4. ✅ Add your own data
5. ✅ Deploy to PythonAnywhere or Heroku
6. ✅ Share your deployed URL

## 📞 Need Help?

- Check `README.md` for detailed documentation
- Review `DEPLOYMENT.md` for deployment issues
- Consult Flask/SQLAlchemy documentation
- Ask your TA or instructor

---

**Happy Coding! 🚀**

