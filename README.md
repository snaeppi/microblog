# Microblog Application

## Description

Microblog is a simple web-based microblogging platform developed with Django. This application is designed for Introduction to Cybersecurity course to demonstrate common web security vulnerabilities. It allows users to create posts, edit posts, and search for posts by their content.

### Vulnerabilities

1. **Broken Access Control (A01:2021)**: Logged-in users can edit any post, not just their own, due to missing ownership verification.

2. **Cryptographic Failures (A02:2021)**: User passwords are stored in plain text in the database.

3. **Injection (A03:2021)**: The application's search functionality and login process are vulnerable to SQL injection.

4. **Security Misconfiguration (A05:2021)**: The application runs with Django's debug mode enabled, which can leak sensitive information.

5. **Identification and Authentication Failures (A07:2021)**: The application has weak (no) password policies allowing easy-to-guess passwords.

## Setup and Configuration

### Prerequisites

- Python 3.x
- Git (for cloning the repository and switching branches)
- pip (for installing Django)

### Clone the Repository

```bash
git clone https://github.com/snaeppi/microblog.git
cd microblog
```

### Install Django

```bash
pip install django
```

### Database Initialization

To initialize the database for different versions of the application:

1. **Switch Branches**
   - For the vulnerable version: `git checkout main`
   - For the fixed version: `git checkout fixed`

2. **Delete Existing Database**
   - Remove the existing SQLite database file: `rm db.sqlite3`

3. **Apply Migrations**
   - Create database schema: `python manage.py migrate`

4. **Initialize Data**
   - Populate the database with initial data: `python manage.py initialize`

### Running the Application

Start the Django development server:

```bash
python manage.py runserver
```

Access the application at `http://127.0.0.1:8000/`.

## Using the Application

### Unsecure Version (main branch)

  - You can register new users, create posts, edit any posts, and use the search functionality to demonstrate SQL injection.
  - To log in as admin, input the following "password": 
  ```
  ' OR username = 'admin' AND '1'='1
  ```
  - To render (username, password) pairs instead of posts, input in the search field: 
  ```
  no-post-contains-this-string%' UNION SELECT id, id, username, password FROM posts_user WHERE '%'=' 
  ```

  - To edit a post that the logged-in user does not own, navigate to `http://127.0.0.1:8000/edit/<post_id>/`, the ids of the posts are in the posting order: first=1, second=2, ...
  - Input `'` to the search field to see a debug error message with a full traceback. 

### Fixed Version (fixed branch)
   - Test all of the above and see that they no longer work.
   - Try creating a user with a weak password.
   - Navigate to a page that does not exist, e.g. `http://127.0.0.1:8000/no_such_page` and verify that the debug error message is not displayed.

