from flask import Flask, request, render_template
from flask_mysqldb import MySQL
from flask_cors import CORS
from urllib.parse import quote_plus 


app = Flask(__name__)
CORS(app)

# Configure MySQL
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mysql123##'
app.config['MYSQL_DB'] = 'student'
app.config['MYSQL_HOST'] = 'localhost'

mysql = MySQL(app)

@app.context_processor
def utility_processor():
    return dict(quote_plus=quote_plus)

@app.route('/')
def display_students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    rv = cur.fetchall()
    
    # Assuming the corrected mapping of ID, Name, and Email columns
    students = [{'ID': row[2], 'Name': row[0], 'Email': row[1]} for row in rv]
    
    cur.close()
    return render_template('index.html', students=students)


# Route for adding a new student
@app.route('/add', methods=['POST'])
def add_student():
    data = request.form
    name = data.get('name')
    email = data.get('email')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO students(studentName, email) VALUES(%s, %s)", (name, email))
    mysql.connection.commit()
    cur.close()
    return display_students()

# Route for updating a student (GET method)
@app.route('/update/<int:student_id>', methods=['GET'])
def update_student_form(student_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE studentID = %s", (student_id,))
    student = cur.fetchone()
    cur.close()
    return render_template('update.html', student=student, student_id=student_id)

# Route for updating a student (POST method)
@app.route('/update/<int:student_id>', methods=['POST'])
def update_student(student_id):
    data = request.form
    updated_name = data.get('name')
    updated_email = data.get('email')
    cur = mysql.connection.cursor()
    cur.execute("UPDATE students SET studentName = %s, email = %s WHERE studentID = %s", (updated_name, updated_email, student_id))
    mysql.connection.commit()
    cur.close()
    return display_students()
# Route for deleting a student
# Route for deleting a student
@app.route('/delete/<string:student_id>', methods=['POST', 'DELETE'])  # Allow both POST and DELETE methods
def delete_student(student_id):
    if request.method == 'POST' or request.method == 'DELETE':
        # Extract the student ID from the URL
        extracted_student_id = student_id

        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM students WHERE studentID = %s", (extracted_student_id,))
        mysql.connection.commit()
        cur.close()
        return display_students()
    else:
        return "Method not allowed", 405  # Return a 405 Method Not Allowed status for unsupported methods

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

