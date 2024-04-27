## Task_Tracking_Project: README.md (English Version)

### Project Description

Task_Tracking_Project is a task management system developed for educational purposes to learn the basics of the Django framework. It allows users to create, edit, delete, and comment on tasks, assign statuses, priorities, and deadlines.

### Functionality

* Authentication and registration: New users can register in the system, while existing users can log in with their username and password. 
* Task management:
    * Create tasks with name, description, status, priority, and deadline.
    * Edit and delete existing tasks.
    * Filter tasks by various criteria (status, priority, deadline).
* Comments: Ability to add comments to tasks for discussing details between users.
* Roles and permissions: Implementation of a permission system to restrict access to editing and deleting tasks.

### Technical Details

* Programming language: Python 3.x
* Framework: Django (latest stable version)
* Database: SQLite (for development), PostgreSQL (for production)
* Frontend: HTML, CSS (Bootstrap), JavaScript
* Development tools: Git, virtualenv/docker

### Installation and Running Instructions

1. Clone the repository:

git clone https://github.com/your-username/Task_Tracking_Project.git


2. Create a virtual environment (optional):

python3 -m venv venv
source venv/bin/activate


3. Install dependencies:

pip install -r requirements.txt


4. Run database migrations:

python manage.py migrate


5. Start the server:

python manage.py runserver


6. Open `http://127.0.0.1:8000/` in your browser.

### License

[No]

### Authors and Contributors

* [Sandy]

### Additional Resources

* [https://www.djangoproject.com/]
* [https://www.python.org/downloads/]


# Task_Tracking_Project 

