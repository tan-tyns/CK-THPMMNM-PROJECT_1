# app.py
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Hàm kết nối Database
def get_db_connection():
    conn = sqlite3.connect('todo.db')
    conn.row_factory = sqlite3.Row
    return conn

# Hàm tạo bảng nếu chưa có (Chạy 1 lần đầu)
def init_db():
    conn = get_db_connection()
    conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, title TEXT)')
    conn.commit()
    conn.close()

# --- ROUTES ---
@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    title = request.form['title']
    conn = get_db_connection()
    conn.execute('INSERT INTO tasks (title) VALUES (?)', (title,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db() # Tự tạo DB khi chạy app
    app.run(host='0.0.0.0', port=5000)