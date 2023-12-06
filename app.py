from flask import Flask, request, json
from flask_mysqldb import MySQL
from flask_cors import CORS

mysql = MySQL()
app = Flask(__name__)
CORS(app)


# MySQL Instance configurations
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_PASSWORD'] = 'Mysql123##'  
app.config['MYSQL_DB'] = 'student'  
app.config['MYSQL_HOST'] = 'localhost'  
 

mysql.init_app(app)
# CREATE - Add a new student
@app.route("/add", methods=['POST'])  # Change method to POST for adding a student
def add():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO students(studentName, email) VALUES(%s, %s)", (name, email))
    mysql.connection.commit()
    cur.close()

    return '{"Result":"Success"}'

# READ - Retrieve all students
@app.route("/")  # Default - Show Data
def read():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    rv = cur.fetchall()
    Results = []
    for row in rv:
        Result = {}
        Result['Name'] = row[0].replace('\n', ' ')
        Result['Email'] = row[1]
        Result['ID'] = row[2]
        Results.append(Result)
    response = {'Results': Results, 'count': len(Results)}
    ret = app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )
    return ret

# UPDATE - Modify a student's details
@app.route("/update/<int:student_id>", methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    updated_name = data.get('name')
    updated_email = data.get('email')
    cur = mysql.connection.cursor()
    cur.execute("UPDATE students SET studentName = %s, email = %s WHERE studentID = %s", (updated_name, updated_email, student_id))
    mysql.connection.commit()
    cur.close()
    return '{"Result":"Success"}'

# DELETE - Remove a student
@app.route("/delete/<int:student_id>", methods=['DELETE'])
def delete_student(student_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE studentID = %s", (student_id,))
    mysql.connection.commit()
    cur.close()
    return '{"Result":"Success"}'






if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080')


