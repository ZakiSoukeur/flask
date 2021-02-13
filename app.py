from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mysql_connector import MySQL
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = 'the random string'
app.config['SECRET_KEY'] = 'the random string'
mysql = MySQL(app)
now = datetime.now()


@app.route('/', methods=['POST', 'GET'])
def index():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        task = request.form['content']
        cur.execute('INSERT INTO todos(content,date_created) VALUES (%s,%s)',
                    (task, now))
        mysql.connection.commit()
        return redirect('/')
    else:

        cur.execute("SELECT * from todos;")
        data = cur.fetchall()
        mysql.connection.commit()
        cur.close()
        return render_template('index.html', data=data)


@app.route('/delete/<int:id>')
def delete(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE from todos where id = %s;', [id])
        mysql.connection.commit()
        flash('User deleted successfully!')
        return redirect('/')
    except Exception as e:
        print(e)
        return 'error'
    finally:
        cur.close()


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from todos where id=%s", [id])
    task = cur.fetchone()
    if request.method == 'POST':
        updatedTask = request.form['content']
        cur.execute("UPDATE todos SET content=%s WHERE id=%s",
                    (updatedTask, id))
        mysql.connection.commit()
        flash('User updated successfully!')
        return redirect('/')

    else:

        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
