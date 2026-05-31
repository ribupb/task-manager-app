# Task Manager Application

A simple Task Manager web application built using Flask, SQLite and Bootstrap. This application allows users to register, log in, and manage tasks through Todo, In Progress, and Done stages.

## Features

- User Registration
- User Login & Logout
- Create Tasks
- Edit Tasks
- Delete Tasks
- Move Tasks between:
  - Todo
  - In Progress
  - Done
- User-specific task management

## Tech Stack

- Python
- Flask
- SQLite
- HTML
- CSS
- Bootstrap

## Installation

1. Clone the repository

```bash
git clone <repository-link>
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Create database

```bash
python database.py
```

4. Run application

```bash
python app.py
```

## Assumptions

- Each user can manage only their own tasks.
- SQLite is used for simplicity and local storage.

## Tradeoffs

- SQLite chosen instead of MySQL/PostgreSQL for faster setup.
- Basic authentication implemented for assignment purposes.

## Technical Decisions

- Flask used as backend framework.
- SQLite used as lightweight database.
- Bootstrap used for responsive UI.
- Session-based authentication implemented.
