import sqlite3
from flask import Flask

app = Flask(__name__)

@app.route('/')
def inspect_db():
    try:
        conn = sqlite3.connect('bank_secure.db')
        cursor = conn.cursor()
        
        # محاولة جلب أسماء الأعمدة من جدول اسمه 'users'
        cursor.execute("PRAGMA table_info(users);")
        columns = cursor.fetchall()
        
        if not columns:
            return "<h1>الجدول 'users' غير موجود أو فارغ!</h1>"
            
        return f"<h1>أسماء الأعمدة الموجودة في الجدول هي: {columns}</h1>"
    except Exception as e:
        return f"<h1>حدث خطأ: {str(e)}</h1>"
