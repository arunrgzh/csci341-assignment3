# Deployment Guide - Caregiver Management System

This guide covers deploying the Flask CRUD application to various hosting platforms.

## 📋 Prerequisites

Before deploying, ensure you have:
- A PostgreSQL database (local or cloud-hosted)
- Application files ready (app.py, models.py, forms.py, config.py, templates/, static/)
- requirements.txt with all dependencies
- Database schema created (create_tables.sql)

## 🌐 Deployment Options

### Option 1: PythonAnywhere (Free Tier Available)

PythonAnywhere offers a free tier perfect for educational projects.

#### Step 1: Create Account
1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free Beginner account
3. Verify your email

#### Step 2: Upload Files
1. Go to **Files** tab
2. Create a new directory: `csci341-assignment3`
3. Upload all project files:
   - app.py, models.py, forms.py, config.py
   - requirements.txt, Procfile
   - templates/ folder (all HTML files)
   - static/ folder (style.css)

#### Step 3: Set Up Virtual Environment
Open a **Bash console** and run:
```bash
cd csci341-assignment3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 4: Configure Database
1. Go to **Databases** tab
2. Create a PostgreSQL database (if available on your plan)
3. Note the connection details
4. Update `config.py` with your database URL:
```python
SQLALCHEMY_DATABASE_URI = "postgresql://username:password@host:port/database"
```

Alternatively, use environment variables in the Web tab.

#### Step 5: Initialize Database
In the Bash console:
```bash
psql -h hostname -U username -d database -f create_tables.sql
psql -h hostname -U username -d database -f insert_data.sql
```

#### Step 6: Configure Web App
1. Go to **Web** tab
2. Click **Add a new web app**
3. Choose **Manual configuration**
4. Select **Python 3.10** (or latest available)
5. Configure:

**Source code:** `/home/yourusername/csci341-assignment3`

**Working directory:** `/home/yourusername/csci341-assignment3`

**Virtualenv:** `/home/yourusername/csci341-assignment3/venv`

**WSGI configuration file:** Edit the file and replace contents with:
```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/csci341-assignment3'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Set environment variables
os.environ['DATABASE_URL'] = 'postgresql://username:password@host:port/database'
os.environ['SECRET_KEY'] = 'your-secret-key-here'

# Import Flask app
from app import app as application
```

#### Step 7: Static Files
In the Web tab, configure static files:
- URL: `/static/`
- Directory: `/home/yourusername/csci341-assignment3/static/`

#### Step 8: Reload and Test
1. Click **Reload** button
2. Visit your app at: `yourusername.pythonanywhere.com`

---

### Option 2: Heroku

Heroku is a popular cloud platform (requires credit card for verification, but has free tier options).

#### Step 1: Install Heroku CLI
Download and install from [heroku.com/cli](https://devcenter.heroku.com/articles/heroku-cli)

#### Step 2: Login
```bash
heroku login
```

#### Step 3: Create Heroku App
```bash
cd csci341-assignment3
heroku create your-app-name
```

#### Step 4: Add PostgreSQL
```bash
heroku addons:create heroku-postgresql:mini
```

This sets the `DATABASE_URL` environment variable automatically.

#### Step 5: Set Environment Variables
```bash
heroku config:set SECRET_KEY=your-secret-key-here
```

#### Step 6: Update config.py
Ensure `config.py` reads from environment variables (already configured):
```python
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "...")
SECRET_KEY = os.getenv("SECRET_KEY", "...")
```

**Important**: Heroku's PostgreSQL URL starts with `postgres://` but SQLAlchemy requires `postgresql://`. Add this to `config.py`:
```python
database_url = os.getenv("DATABASE_URL", "...")
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)
SQLALCHEMY_DATABASE_URI = database_url
```

#### Step 7: Create Procfile
Already included in project:
```
web: gunicorn app:app
```

#### Step 8: Initialize Git (if not already)
```bash
git init
git add .
git commit -m "Initial commit"
```

#### Step 9: Deploy
```bash
git push heroku main
# or if your branch is master:
git push heroku master
```

#### Step 10: Initialize Database
```bash
heroku pg:psql < create_tables.sql
heroku pg:psql < insert_data.sql
```

#### Step 11: Open App
```bash
heroku open
```

Your app will be available at: `https://your-app-name.herokuapp.com`

---

### Option 3: AWS (Amazon Web Services) - Educational Tier

AWS offers free tier for students through AWS Educate.

#### Step 1: Sign Up
1. Go to [aws.amazon.com/education](https://aws.amazon.com/education/awseducate/)
2. Sign up with your @nu.edu.kz email
3. Access AWS Console

#### Step 2: Launch EC2 Instance
1. Go to EC2 Dashboard
2. Launch Instance (Ubuntu 22.04 LTS)
3. Choose t2.micro (free tier eligible)
4. Configure security group:
   - SSH (port 22)
   - HTTP (port 80)
   - HTTPS (port 443)
   - Custom TCP (port 5000 for testing)

#### Step 3: Connect to Instance
```bash
ssh -i your-key.pem ubuntu@your-instance-ip
```

#### Step 4: Install Dependencies
```bash
sudo apt update
sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx -y
```

#### Step 5: Set Up PostgreSQL
```bash
sudo -u postgres psql
CREATE DATABASE caregivers;
CREATE USER youruser WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE caregivers TO youruser;
\q
```

#### Step 6: Upload Project Files
Use SCP or Git:
```bash
# On your local machine
scp -i your-key.pem -r csci341-assignment3 ubuntu@your-instance-ip:~/

# Or clone from Git
ssh -i your-key.pem ubuntu@your-instance-ip
git clone your-repo-url csci341-assignment3
```

#### Step 7: Set Up Application
```bash
cd csci341-assignment3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Step 8: Configure Database
Update `config.py` with your PostgreSQL credentials.

Initialize database:
```bash
psql -U youruser -d caregivers -f create_tables.sql
psql -U youruser -d caregivers -f insert_data.sql
```

#### Step 9: Run with Gunicorn
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

#### Step 10: Configure Nginx (Optional, for production)
Create `/etc/nginx/sites-available/caregivers`:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /home/ubuntu/csci341-assignment3/static;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/caregivers /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 11: Set Up Systemd Service (Keep app running)
Create `/etc/systemd/system/caregivers.service`:
```ini
[Unit]
Description=Caregiver Management System
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/csci341-assignment3
Environment="PATH=/home/ubuntu/csci341-assignment3/venv/bin"
ExecStart=/home/ubuntu/csci341-assignment3/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable caregivers
sudo systemctl start caregivers
```

---

## 🔐 Security Checklist

Before deploying to production:

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS (use Let's Encrypt for free SSL)
- [ ] Set `DEBUG = False` in production
- [ ] Use strong database passwords
- [ ] Restrict database access to application server only
- [ ] Set up firewall rules
- [ ] Regular backups of database
- [ ] Implement rate limiting
- [ ] Add authentication/authorization if needed

## 🔧 Environment Variables

Set these environment variables on your hosting platform:

```bash
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=False  # Set to False in production
```

## 📊 Database Management

### Backup Database
```bash
pg_dump -U username -d caregivers > backup.sql
```

### Restore Database
```bash
psql -U username -d caregivers < backup.sql
```

### Reset Database
```bash
psql -U username -d caregivers -f create_tables.sql
psql -U username -d caregivers -f insert_data.sql
```

## 🐛 Troubleshooting

### Application won't start
- Check logs: `heroku logs --tail` (Heroku) or check PythonAnywhere error log
- Verify all dependencies are installed
- Check DATABASE_URL is set correctly

### Database connection errors
- Verify database credentials
- Check if database server is accessible
- Ensure PostgreSQL is running

### Static files not loading
- Check static files configuration in web server
- Verify file paths are correct
- Check file permissions

### Import errors
- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`
- Check Python version compatibility

## 📞 Support

For deployment issues:
- PythonAnywhere: [help.pythonanywhere.com](https://help.pythonanywhere.com)
- Heroku: [devcenter.heroku.com](https://devcenter.heroku.com)
- AWS: [aws.amazon.com/support](https://aws.amazon.com/support)

## 📚 Additional Resources

- [Flask Deployment Options](https://flask.palletsprojects.com/en/latest/deploying/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Gunicorn Documentation](https://docs.gunicorn.org/)
- [Nginx Configuration](https://nginx.org/en/docs/)
