# CampusFlow College ERP

A starter College ERP application built with Flask + MySQL.

## Features included

- Student, Faculty and Admin roles
- Secure password hashing
- Login/logout
- Responsive dashboard
- Student assignment view
- Faculty assignment creation
- Faculty student list
- Student-faculty message data model
- MySQL database integration
- Mobile-responsive UI

## Setup

1. Install Python 3.11+.
2. Install MySQL.
3. Create a database named `college_erp`.
4. Edit `config.py` and replace `YOUR_MYSQL_PASSWORD`.
5. Open a terminal in this folder.
6. Run:

   python -m venv venv

   Windows:
   venv\Scripts\activate

   macOS/Linux:
   source venv/bin/activate

   pip install -r requirements.txt

7. Start:

   python app.py

8. Open:

   http://127.0.0.1:5000

## Demo login

Student:
student@erp.com
student123

Faculty:
faculty@erp.com
faculty123

Admin:
admin@erp.com
admin123
