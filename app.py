import os
import sqlite3
import requests  
from flask import Flask, render_template, request, redirect, url_for, session
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = os.urandom(24)

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

DATABASE = 'bank_secure.db'
STATIC_INTRUDER_IMG = '/static/intruders/default_hacker.jpg'  

def send_security_alert(ip, username, action):
    """📢 دالة بنكية لإرسال تنبيه فوري لفريق الأمن (تليجرام / بريد إلكتروني)"""
    bot_token = "YOUR_BOT_TOKEN"
    chat_id = "YOUR_CHAT_ID"
    message = f"⚠️ **تنبيه أمني عاجل - رادار البنك** ⚠️\n\n🌐 مصدر الهجوم (IP): {ip}\n👤 المدخل المستخدم: {username}\n🛡️ إجراء النظام: {action}"
    
    if bot_token != "YOUR_BOT_TOKEN":
        try:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            requests.post(url, json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"})
        except Exception as e:
            print(f"تنبيـه: فشل إرسال الإشعار الفوري: {e}")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """إنشاء البنية التحتية لقاعدة البيانات وحقن حساب مظهر (VIP) المشفر"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY, name TEXT NOT NULL, password_hash TEXT NOT NULL, role TEXT NOT NULL, account_type TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, detail TEXT NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS security_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, ip_address TEXT, username_entered TEXT, action_taken TEXT, image_path TEXT
        )
    ''')

    hashed_pw = generate_password_hash("123", method='pbkdf2:sha256')
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?, ?, ?)", 
                   ('mazhar_cyber', 'مظهر', hashed_pw, 'عميل متميز (VIP)', 'حساب استثماري نشط'))
    
    cursor.execute("INSERT OR IGNORE INTO accounts (id, user_id, detail) VALUES (1, 'mazhar_cyber', 'الحساب الجاري: 450,000 SAR')")
    cursor.execute("INSERT OR IGNORE INTO accounts (id, user_id, detail) VALUES (2, 'mazhar_cyber', 'المحفظة الاستثمارية: 1,200,000 SAR')")
    cursor.execute("INSERT OR IGNORE INTO accounts (id, user_id, detail) VALUES (3, 'mazhar_cyber', 'الودائع لأجل: 300,000 SAR')")
        
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=["GET", "POST"])
@limiter.limit("5 per minute", error_message="🚨 تم حظر الـ IP الخاص بك مؤقتاً لتجاوز حد محاولات الدخول المسموحة (حماية Brute Force).")
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        ip_addr = request.remote_addr

        malicious_patterns = ["'", '"', "--", "OR", "AND", "or", "and", "SELECT", "select"]
        if any(pattern in username for pattern in malicious_patterns) or any(pattern in password for pattern in malicious_patterns):
            
            action = "❌ محاولة اختراق محجوبة (حقن ثغرة SQLi)"
            
            conn = get_db_connection()
            conn.execute("INSERT INTO security_logs (ip_address, username_entered, action_taken, image_path) VALUES (?, ?, ?, ?)",
                         (ip_addr, username, action, STATIC_INTRUDER_IMG))
            conn.commit()
            conn.close()
            
            send_security_alert(ip_addr, username, action)
            return "... تم حظر محاولتك بنجاح. تم تسجيل هويتك الرقمية وصورتك في رادار نظام المؤسسة 403 ⚠️"

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE id = ?", (username,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['role'] = user['role']
            session['account_type'] = user['account_type']
            
            conn = get_db_connection()
            conn.execute("INSERT INTO security_logs (ip_address, username_entered, action_taken, image_path) VALUES (?, ?, ?, ?)",
                         (ip_addr, username, "✅ دخول ناجح واستعراض البيانات الحساسة", None))
            conn.commit()
            conn.close()
            return redirect(url_for('dashboard'))
        else:
            action = "👤 شخص غريب حاول الدخول وتم طرده"
            
            conn = get_db_connection()
            conn.execute("INSERT INTO security_logs (ip_address, username_entered, action_taken, image_path) VALUES (?, ?, ?, ?)",
                         (ip_addr, username, action, STATIC_INTRUDER_IMG))
            conn.commit()
            conn.close()
            
            send_security_alert(ip_addr, username, action)
            return "❌ الحساب المدخل غير مسجل في أنظمتنا الأمنية المصرفية."

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    accounts = conn.execute("SELECT detail FROM accounts WHERE user_id = ?", (session['user_id'],)).fetchall()
    conn.close()
    return render_template('dashboard.html', accounts=accounts)

@app.route('/admin_panel_secure_v1')
def admin_panel():
    conn = get_db_connection()
    logs = conn.execute("SELECT timestamp, ip_address, username_entered, action_taken, image_path FROM security_logs ORDER BY id DESC").fetchall()
    conn.close()
    return render_template('admin_panel.html', logs=logs)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':

