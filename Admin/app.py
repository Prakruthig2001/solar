from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
import pymysql

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # needed for flashing

# Configure MySQL
db = pymysql.connect(
    host="localhost",
    user="root",
    password="Anjali@123",
    database="solar_panel_washer",
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main/Admin/templates/auto.html')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # Process or store the message
    flash("Your message has been sent!", "success")
    return redirect(url_for('contact'))


@app.route('/auto')
def auto():
    return render_template('auto.html')

@app.route('/manual')
def manual():
    return render_template('manual.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/profile')
def profile():
    user_id = 1  # Normally you'd get this from session
    with db.cursor() as cursor:
        cursor.execute("SELECT id, name, email, phone, address, role FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
    return render_template('profile.html', user=user)

@app.route('/change_password', methods=['POST'])
def change_password():
    user_id = 1  # Get from session in real app
    current = request.form['current_password']
    new = request.form['new_password']
    confirm = request.form['confirm_password']

    if new != confirm:
        flash("New passwords do not match.", "danger")
        return redirect(url_for('profile'))

    with db.cursor() as cursor:
        cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
        stored = cursor.fetchone()

        if stored and check_password_hash(stored['password'], current):
            new_hashed = generate_password_hash(new)
            cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_hashed, user_id))
            db.commit()
            flash("Password updated successfully.", "success")
        else:
            flash("Current password is incorrect.", "danger")

    return redirect(url_for('profile'))

if __name__ == '__main__':
    app.run(debug=True)
