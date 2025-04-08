# 💼 Job Searching Portal

A web-based Job Searching Portal built using Django. This platform allows admins to post job listings and users to apply for jobs. It features user authentication, job application management, and more — all in a simple and functional design.

## ✨ Features

- ✅ Admin can add and delete job listings
- ✅ Users can register, log in, and apply for jobs
- ✅ Admin can view all applied jobs
- ✅ Save/unsave jobs functionality
- ✅ Notification system with delete option
- ✅ Password change functionality
- ✅ Clean and simple HTML templates
- ✅ Basic success page after actions
- ✅ Data is persisted in the database

## 🔐 Login Credentials (for testing)

| Role  | Username | Password |
|-------|----------|----------|
| Admin | admin    | admin    |
| User  | user     | user     |
| User  | user1    | user1    |

## 🔧 Tech Stack

- Python
- Django
- SQLite (default database)

## 🚀 How to Run Locally

```bash
# Clone the repository (replace with your repo URL)
git clone https://github.com/your-username/jobsearch-portal.git
cd jobsearch-portal

# Set up virtual environment
python -m venv myenv

# Activate the environment (Windows)
myenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run the server
python manage.py runserver
