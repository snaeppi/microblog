# Microblog Application

## Description

Microblog is a simple web-based microblogging platform developed with Django. This application is designed for Introduction to Cybersecurity course to demonstrate common web security vulnerabilities. It allows users to create posts, edit posts, and search for posts by their content.

### Vulnerabilities

1. **Broken Access Control (A01:2021)**: Logged-in users can edit any post, not just their own, due to missing ownership verification.

2. **Cryptographic Failures (A02:2021)**: User passwords are stored in plain text in the database.

3. **Injection (A03:2021)**: The application's search functionality and login process are vulnerable to SQL injection.

4. **Security Misconfiguration (A05:2021)**: The application runs with Django's debug mode enabled, which can leak sensitive information.

5. **Identification and Authentication Failures (A07:2021)**: The application has weak (no) password policies allowing easy-to-guess passwords.

## Installation

1. **Clone the Repository**
    ```bash
    git clone https://your-repository-url/microblog.git
    cd microblog
    ```

2. **Set Up a Virtual Environment** (Optional but recommended)
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Django**
    ```bash
    pip install django
    ```

4. **Migrate Database**
    ```bash
    python manage.py migrate
    ```

5. **Create users**
    ```bash
    python manage.py create_users
    ```

## Running the Application

1. **Start the Django Development Server**
    ```bash
    python manage.py runserver
    ```

2. **Access the Application**
    - Open a web browser and navigate to `http://127.0.0.1:8000/`.

3. **Using the Application**
    - You can register new users, create posts, edit any posts, and use the search functionality to demonstrate SQL injection.
    - To log in as admin, input the following "password": `' OR username = 'admin' AND '1'='1`
    - To render username: password pairs instead of posts, search for: `no-post-contains-this-string%' UNION SELECT id, id, username, password FROM posts_user WHERE '%'='`

