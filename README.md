# govtech-assassment-2
Coding Assignment: **Financial Assistance Scheme Management System (FASMS)**

## Overview

The FASMS is a backend system designed to manage financial assistance schemes for individuals and families. It facilitates the management of schemes, administrator accounts, applicant records, and determines applicant eligibility for various schemes.

## Project Directory

```
├─ README.md
├─ requirements.txt
│
├─ manage.py
│
├─ govtech_fasms/
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│
├─ accounts/
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ migrations/
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ serializers.py
│  ├─ urls.py
│  ├─ views.py
│  ├─ tests.py
│
├─ applicants/
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ migrations/
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ serializers.py
│  ├─ urls.py
│  ├─ views.py
│  ├─ tests.py
│
├─ schemes/
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ migrations/
│  │  └─ __init__.py
│  ├─ models.py
│  ├─ serializers.py
│  ├─ urls.py
│  ├─ views.py
│  ├─ tests.py
│
└─ applications/
   ├─ __init__.py
   ├─ admin.py
   ├─ apps.py
   ├─ migrations/
   │  └─ __init__.py
   ├─ models.py
   ├─ serializers.py
   ├─ urls.py
   ├─ views.py
   ├─ tests.py


```


## Features

- **Scheme Management:** Create, update, and delete financial assistance schemes.
- **Administrator Management:** Handle administrator accounts with secure authentication.
- **Applicant Records:** Store and update applicant information and their household details.
- **Eligibility Assessment:** Advise on schemes each applicant is eligible to apply for.
- **Application Tracking:** Record the outcomes of applications submitted by applicants.

## Tech Stack

- **Backend Language:** Python 3.12.7
- **Backend Framework:** Django 5.1.4
- **Database:** PostgreSQL 17.2.2
- **API Documentation:** Postman 11.21.0
- **Authentication:** Django built-in authentication

## Prerequisites

- [**Python 3.12.7**](https://www.python.org/ftp/python/3.12.7/python-3.12.7-amd64.exe "Download Python 3.12.7")
- [**PostgreSQL 17.2.2**](https://sbp.enterprisedb.com/getfile.jsp?fileid=1259295 "Download PostgreSQL 17.2.2")

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/Benhzy/govtech-assassment-2.git
   ```

2. **Create a Virtual Environment:**

   Run the following command to create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. **Activate the Virtual Environment:**

   ```bash
   .venv\Scripts\activate
   ```

   You should see `(.venv)` at the begstartinning of your terminal prompt.

4. **Install Dependencies:**

   Run the following command to install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Database:**

   Login to your PostgreSQL command-line interface using the following command:
   
   ```bash
   psql -U <username> -h <host> -d <database_name>
   ```

   Run the following command to create the required database:

   ```sql
   CREATE DATABASE fasms;
   ```
   Update your `.env` file with the following database parameters:

   ```env
   DB_NAME=fasms
   DB_USER=username
   DB_PASSWORD=password
   DB_HOST=localhost
   DB_PORT=5432
   ```
   Replace `username` and `password` with your PostgreSQL credentials.
   `DB_HOST` and `DB_PORT` should be updated for production environment.

   Migrate models into Postgres database using the following commands:

   ```bash
   cd .\govtech_fasms\
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run Development Mode**

   Run the following command to start the Django development server:

   ```bash
   python manage.py runserver localhost:5000
   ```

6. **Administrator Management**

   Run the following command to create an administrator user:

   ```bash
   python manage.py createsuperuser
   ```

   