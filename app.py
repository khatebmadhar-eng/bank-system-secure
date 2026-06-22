from flask import Flask, request, render_template_string

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# واجهة تسجيل الدخول
LOGIN_PAGE = '''
<div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
    <h2>تسجيل الدخول للنظام البنكي</h2>
    <p style="color: red;">{{ message }}</p>
    <form method="POST" action="/">
        <input type="text" name="username" placeholder="اسم المستخدم" required><br><br>
        <input type="password" name="password" placeholder="كلمة المرور" required><br><br>
        <input type="submit" value="تسجيل الدخول">
    </form>
</div>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # التحقق من البيانات (سنربطها بقاعدة البيانات لاحقاً)
        if username == 'admin' and password == '1234':
            return "<h1>تم تسجيل الدخول بنجاح!</h1>"
        else:
            message = "اسم المستخدم أو كلمة المرور غير صحيحة!"
            
    return render_template_string(LOGIN_PAGE, message=message)
