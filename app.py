import sqlite3
import os
from flask import Flask, request

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        db_path = 'bank_secure.db'
        
        if not os.path.exists(db_path):
            return f"<h1>خطأ: ملف قاعدة البيانات غير موجود في المسار: {os.path.abspath(db_path)}</h1>"
            
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return "<h1>تم تسجيل الدخول بنجاح!</h1>"
            else:
                return "<h1>اسم المستخدم أو كلمة المرور غير صحيحة.</h1>"
        except Exception as e:
            return f"<h1>حدث خطأ تقني: {str(e)}</h1>"
    
    return '''
        <form method="post">
            <h2>تسجيل الدخول للنظام البنكي</h2>
            <input type="text" name="username" placeholder="اسم المستخدم" required><br><br>
            <input type="password" name="password" placeholder="كلمة المرور" required><br><br>
            <input type="submit" value="تسجيل الدخول">
        </form>
    '''
