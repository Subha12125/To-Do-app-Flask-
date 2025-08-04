from flask import Blueprint, render_template, request, redirect, url_for, flash, session

auth_bp = Blueprint('auth', __name__)

# In production, move these to environment variables or a secure config
USER_CREDENTIALS = {
    'username': 'admin',
    'password': '1234'
}

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Basic validation
        if not username or not password:
            flash("Please fill in all fields.", "danger")
            return render_template('login.html')

        if username == USER_CREDENTIALS['username'] and password == USER_CREDENTIALS['password']:
            session['user'] = username
            flash("Login successful! Welcome to your To-Do App.", "success")
            return redirect(url_for('tasks.view_tasks'))
        else:
            flash("Invalid username or password. Please try again.", "danger")

    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out successfully.", "info")
    return redirect(url_for('auth.login'))