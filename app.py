
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL, MySQLdb
import MySQLdb.cursors
import re
import camera
import sms
import os

app = Flask(__name__)
app.secret_key = 'mykeys'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'cbt_data'

mysql = MySQL(app)
    

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    msg = ''
    username = "Admin"
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST' and 'question' in request.form and 'optionA' in request.form and 'answer' in request.form:
        question = request.form['question']
        optionA = request.form['optionA']
        optionB = request.form['optionB']
        optionC = request.form['optionC']
        optionD = request.form['optionD']
        answer = request.form['answer']
        
        cursor.execute(
                    'INSERT INTO questions VALUES (NULL, %s, %s, %s, %s, %s, %s)', (question, optionA, optionB, optionC, optionD, answer))
        mysql.connection.commit()
        msg = 'Question successfully saved'
    elif request.method == 'POST':
        msg = 'Please fill entire field!'
        
    return render_template('admin.html', mess = msg, username = username)

@app.route('/delete', methods=['POST', 'GET'])
def delete():
    msg = ''
    username = 'Admin'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST' and 'number' in request.form:
        num = request.form['number']
        cursor.execute(
                    'DELETE FROM questions WHERE id = %s'%num )
        mysql.connection.commit()
        msg = 'Question successfully deleted'
    elif request.method == 'POST':
        msg = 'Please enter a valid number!'
        
    return render_template('deletequestion.html', mess = msg, username = username)
  
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST'  and 'password' in request.form and 'username' in request.form:
        const_username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM account WHERE username = %s AND password = %s', (const_username, password))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['email'] = account['email']
            session['phone_no'] = account['phone_no']
            
            #return redirect(url_for('face'))
            return redirect(url_for('exam'))
        else:
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg= msg)


@app.route('/facial', methods=['GET', 'POST'])
def face():
    msg = ''
    if request.method == 'POST':
      
        name, result = camera.detectface()
        if name == session['username'].upper():
            
            if result == "authentication successful":
                return redirect(url_for('exam'))
            else:
                msg = "authentication failed"
        else:
                msg = "face id failed"
     
    
    return render_template('face.html', msg= msg)


@app.route('/exam', methods = ['POST', 'GET'])
def exam():
    if 'loggedin' in session:
        questions = ''
        score = 0
        que = []
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM questions')
        questions = cursor.fetchall()
        
        if request.method == 'POST':  
            phone = session['phone_no']
            id = session["id"] 
            print(phone)
            for q in questions:
                user_answer = request.form.getlist(q['question'])
                if len(user_answer) > 0:
                    if q['answer'] == user_answer[0]:
                        score += 4
                        print(score)
                    else:
                        score += 0
                else:
                    score = 0
                    print("score is 0")
            cursor.execute("UPDATE account set `score` = %s WHERE id = %s", (score, id))
            mysql.connection.commit()
            
            score_message = "Entrance_Exam_Score:%s" %score 
            #try
            sms.sending_sms(phone, score_message)
            session.pop('loggedin', None)
            session.pop('id', None)
            session.pop('username', None)
            #except:
                #return redirect(url_for('error'))
            
            return redirect(url_for('exam_success'))
    
        return render_template('exam.html', username = session['username'], questions = questions, que=que)
    return redirect(url_for('login'))

@app.route('/error')
def error():
    return render_template('error.html')
    

@app.route('/exam_success', methods=['POST', 'GET'])
def exam_success():
    if 'loggedin' in session:
        return render_template('exam_score.html')
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        phone_no = request.form['phone_no']
        score = 0

        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM account WHERE username = %s OR password = %s', (username, password))
        account = cursor.fetchone()

        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg == 'Please fill out the form!'
        else:
            uploaded_file = request.files['file']
            if uploaded_file.filename != '':
                uploaded_file.filename = "%s.jpg"%username
                file_dir = 'images/'
                real_dir = file_dir+uploaded_file.filename
                uploaded_file.save(real_dir)
                cursor.execute(
                    'INSERT INTO account VALUES (NULL, %s, %s, %s, %s, %s)', (username, password, email, phone_no, score))
                mysql.connection.commit()
                msg = 'You have successfully registered'
                return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form!'

    return render_template('register.html', msg=msg)



app.run(host='localhost', port=8000, debug=True)
