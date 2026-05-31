from flask import Flask, render_template, request, session, redirect
import sqlite3

app = Flask(__name__)
app.secret_key = "taskmanagersecret"



@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=?",
            (email,)
        )

        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()

            return render_template(
                'register.html',
                error="Email already exists"
            )

        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:
            session['user_id'] = user[0]
            return redirect('/dashboard')

        return render_template(
            'login.html',
            error="Invalid Email or Password"
        )

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT * FROM tasks
        WHERE user_id=?
        """,
        (session['user_id'],)
    )

    tasks = cursor.fetchall()

    todo_count = sum(1 for task in tasks if task[4] == 'Todo')
    progress_count = sum(1 for task in tasks if task[4] == 'In Progress')
    done_count = sum(1 for task in tasks if task[4] == 'Done')

    conn.close()

    return render_template(
        'dashboard.html',
        tasks=tasks,
        todo_count=todo_count,
        progress_count=progress_count,
        done_count=done_count
    )

@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')


@app.route('/add_task', methods=['POST'])
def add_task():

    if 'user_id' not in session:
        return redirect('/login')

    title = request.form['title']
    description = request.form['description']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tasks(user_id,title,description,status)
        VALUES(?,?,?,?)
        """,
        (
            session['user_id'],
            title,
            description,
            'Todo'
        )
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')

@app.route('/move_task/<int:task_id>/<status>', methods=['POST'])
def move_task(task_id, status):
    
    if 'user_id' not in session:
       return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status=? WHERE id=?",
        (status, task_id)
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')

@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    
    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id=?",
        (task_id,)
    )

    conn.commit()
    conn.close()

    return redirect('/dashboard')


@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):

    if 'user_id' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']

        cursor.execute(
            """
            UPDATE tasks
            SET title=?, description=?
            WHERE id=?
            """,
            (title, description, task_id)
        )

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    cursor.execute(
        "SELECT * FROM tasks WHERE id=?",
        (task_id,)
    )

    task = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_task.html',
        task=task
    )

if __name__ == '__main__':
    app.run(debug=True)