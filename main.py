import psycopg2
from flask import Flask, Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask import (jsonify, request)
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'

@app.route('/')
def main_page():
    return render_template('main.html')

@app.route('/employee')
def employee():
    conn = psycopg2.connect(user="postgres", password="1234", host="127.0.0.1", port="5432", database="pbz_2")
    cur = conn.cursor()
    cur.execute('SELECT * FROM EMPLOYEE')
    table = cur.fetchall()
    conn.close()

    df = pd.DataFrame({'ID сотрудника': [], 'ФИО': [], 'Должность': [], 'Email': [], 'ID организации': []})
    for i in range(len(table)):
        df.loc[len(df.index)] = [table[i][0], table[i][1], table[i][2], table[i][3], table[i][4]]

    df = df.sort_values('ID сотрудника')

    return render_template('employee.html', df=df)

@app.route('/add_emp')
def add_employee_temp():
    return render_template('add_emp.html')

@app.route('/add_emp', methods =["POST"])
def add_employee():
    id = request.form.get('id')
    name = request.form.get('name')
    post = request.form.get('post')
    email = request.form.get('email')
    org_id = request.form.get('org_id')
    connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1",port="5432",database="pbz_2")

    cur = connection.cursor()
    cur.execute(
        f"INSERT INTO EMPLOYEE (ID, NAME, POST, EMAIL, ORGANIZATION_ID) VALUES ({id},'{name}','{post}','{email}',{org_id})"
    )

    connection.commit()
    cur.execute("SELECT * from EMPLOYEE")
    table = cur.fetchall()
    connection.close()

    df = pd.DataFrame({'ID сотрудника': [], 'ФИО': [], 'Должность': [], 'Email': [], 'ID организации': []})
    for i in range(len(table)):
        df.loc[len(df.index)] = [table[i][0], table[i][1], table[i][2], table[i][3], table[i][4]]

    df = df.sort_values('ID сотрудника')


    return render_template("employee.html", df=df)

@app.route('/organization')
def organization():
    conn = psycopg2.connect(user="postgres", password="1234", host="127.0.0.1", port="5432", database="pbz_2")
    cur = conn.cursor()
    cur.execute('SELECT * FROM ORGANIZATION')
    table = cur.fetchall()
    conn.close()

    df = pd.DataFrame({'ID организации': [], 'Название': []})
    for i in range(len(table)):
        df.loc[len(df.index)] = [table[i][0], table[i][1]]

    df = df.sort_values('ID организации')

    return render_template('organization.html', df=df)

@app.route('/add_org')
def add_organization_temp():
    return render_template('add_org.html')

@app.route('/add_org', methods =["POST"])
def add_organization():
    id = request.form.get('id')
    name = request.form.get('name')
    connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1",port="5432",database="pbz_2")

    cur = connection.cursor()

    cur.execute(f"INSERT INTO ORGANIZATION (ID,NAME) VALUES ({id},'{name}');")
    connection.commit()
    cur.execute("SELECT * from ORGANIZATION;")
    table = cur.fetchall()
    connection.close()

    df = pd.DataFrame({'ID организации': [], 'Название': []})
    for i in range(len(table)):
        df.loc[len(df.index)] = [table[i][0], table[i][1]]

    df = df.sort_values('ID организации')

    return render_template('organization.html', df=df)

@app.route('/task')
def task():
    conn = psycopg2.connect(user="postgres", password="1234", host="127.0.0.1", port="5432", database="pbz_2")
    cur = conn.cursor()
    cur.execute('SELECT * FROM TASK')
    table = cur.fetchall()
    conn.close()

    df = pd.DataFrame({'ID задачи': [], 'Название': [], 'ID исполнителя': [], 'Срок исполнения': [], 'ID документа': []})
    for i in range(len(table)):
        df.loc[len(df.index)] = [table[i][0], table[i][1], table[i][2], table[i][3], table[i][4]]

    df = df.sort_values('ID задачи')

    return render_template('task.html', df=df)

@app.route('/add_task')
def add_task_temp():
    return render_template('add_task.html')

@app.route('/add_task', methods =["POST"])
def add_task():
    id = request.form.get('id')
    name = request.form.get('name')
    explorer_id = request.form.get('explorer_id')
    exp_date = request.form.get('exp_date')
    doc_id = request.form.get('doc_id')
    connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1",port="5432",database="pbz_2")

    cur = connection.cursor()

    cur.execute(
        f"INSERT INTO TASK (ID, NAME, EXPLORER_ID, EXP_DATE, DOC_ID) VALUES ({id},'{name}',{explorer_id},'{exp_date}',{doc_id})"
    )

    connection.commit()
    cur.execute("SELECT * from TASK")
    table = cur.fetchall()
    connection.close()

    df = pd.DataFrame({'ID задачи': [], 'Название': [], 'ID исполнителя': [], 'Срок исполнения': [], 'ID документа': []})
    for i in range(len(table)):
        df.loc[len(df.index)] = [table[i][0], table[i][1], table[i][2], table[i][3], table[i][4]]

    df = df.sort_values('ID задачи')

    return render_template('task.html', df=df)

@app.route('/document')
def document():
    conn = psycopg2.connect(user="postgres", password="1234", host="127.0.0.1", port="5432", database="pbz_2")
    cur = conn.cursor()
    cur.execute('SELECT * FROM DOCUMENT')
    table = cur.fetchall()
    conn.close()

    df = pd.DataFrame({'ID документа': [], 'Дата регистрации': [], 'Адресат': [], 'Адресант': [], 'ID автора резолюции': [], 'ID контролера': []})
    for i in range(len(table)):
        df.loc[len(df.index)] = [table[i][0], table[i][1], table[i][2], table[i][3], table[i][4], table[i][5]]

    df = df.sort_values('ID документа')

    return render_template('document.html', df=df)

@app.route('/add_doc')
def add_document_temp():
    return render_template('add_doc.html')

@app.route('/add_doc', methods =["POST"])
def add_document():
    id = request.form.get('id')
    date = request.form.get('date')
    adresat = request.form.get('adresat')
    adresant = request.form.get('adresant')
    res_id = request.form.get('res_id')
    cont_id = request.form.get('cont_id')
    connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1",port="5432",database="pbz_2")

    cur = connection.cursor()
    cur.execute(
        f"INSERT INTO DOCUMENT (ID, REG_DATE, ADRESAT, ADRESANT, RESOLUTION_ID, CONTROLLER_ID) VALUES ({id},'{date}',{adresat},{adresant},{res_id}, {cont_id})"
    )

    connection.commit()
    cur.execute("SELECT * from DOCUMENT")
    table = cur.fetchall()
    connection.close()

    df = pd.DataFrame(
        {'ID документа': [], 'Дата регистрации': [], 'Адресат': [], 'Адресант': [], 'ID автора резолюции': [],
         'ID контролера': []})
    for i in range(len(table)):
        df.loc[len(df.index)] = [table[i][0], table[i][1], table[i][2], table[i][3], table[i][4], table[i][5]]

    df = df.sort_values('ID документа')

    return render_template("document.html", df=df)

@app.route('/update_task')
def update():
    return render_template('update_task.html')

@app.route('/update_task', methods =["POST"])
def update_task():
    id = request.form.get('id')
    exp_id = request.form.get('exp_id')
    connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1",port="5432",database="pbz_2")

    cur = connection.cursor()

    if id == '':
        flash('Введите ID записи!')
        return redirect(url_for('update_task'))

    cur.execute(f'SELECT * FROM TASK WHERE ID = {id}')
    rows = cur.fetchall()

    if exp_id == '':
        exp_id = rows[0][2]


    cur.execute(f"UPDATE TASK set EXPLORER_ID = {exp_id} where ID = {id}")

    connection.commit()

    cur.execute("SELECT * from TASK")
    table = cur.fetchall()
    connection.close()

    df = pd.DataFrame({'ID задачи': [], 'Название': [], 'ID исполнителя': [], 'Срок исполнения': [], 'ID документа': []})
    for i in range(len(table)):
        df.loc[len(df.index)] = [table[i][0], table[i][1], table[i][2], table[i][3], table[i][4]]

    df = df.sort_values('ID задачи')

    return render_template('task.html', df=df)

@app.route('/update_task_date')
def update_date():
    return render_template('update_task_date.html')

@app.route('/update_task_date', methods =["POST"])
def update_task_date():
    id = request.form.get('id')
    exp_date = request.form.get('exp_date')
    connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1",port="5432",database="pbz_2")

    cur = connection.cursor()

    if id == '':
        flash('Введите ID записи!')
        return redirect(url_for('update_task_date'))

    cur.execute(f'SELECT * FROM TASK WHERE ID = {id}')
    rows = cur.fetchall()

    if exp_date == '':
        exp_date = rows[0][3]

    cur.execute(f"UPDATE TASK set EXP_DATE = '{exp_date}' where ID = {id}")

    connection.commit()

    cur.execute("SELECT * from TASK")
    table = cur.fetchall()
    connection.close()

    df = pd.DataFrame({'ID задачи': [], 'Название': [], 'ID исполнителя': [], 'Срок исполнения': [], 'ID документа': []})
    for i in range(len(table)):
        df.loc[len(df.index)] = [table[i][0], table[i][1], table[i][2], table[i][3], table[i][4]]

    df = df.sort_values('ID задачи')

    return render_template('task.html', df=df)


@app.route('/drop')
def drop():
    return render_template('drop.html')

@app.route('/drop', methods =["POST"])
def drop_note():
    if request.form.get('employee'):
        flag = 'EMPLOYEE'
    elif request.form.get('organization'):
        flag = 'ORGANIZATION'
    elif request.form.get('document'):
        flag = 'DOCUMENT'
    elif request.form.get('task'):
        flag = 'TASK'

    id = request.form.get('id')
    connection = psycopg2.connect(user="postgres",password="1234",host="127.0.0.1",port="5432",database="pbz_2")

    cur = connection.cursor()

    if id == '':
        flash('Введите ID записи!')
        return redirect(url_for('drop'))

    cur.execute(f"DELETE FROM {flag} WHERE ID = {id}")

    connection.commit()

    cur.execute("SELECT * from WORKER")
    connection.close()

    return render_template("main.html")

@app.route('/find_task')
def find_task():
    return render_template("find_task.html")

@app.route('/find_task', methods =["POST"])
def find_taskk():
    exp_date1 = request.form.get('exp_date1')
    exp_date2 = request.form.get('exp_date2')
    conn = psycopg2.connect(user="postgres", password="1234", host="127.0.0.1", port="5432", database="pbz_2")
    cur = conn.cursor()

    if exp_date1 == '' or exp_date2 == '':
        flash('Введите дату')
        return redirect(url_for('find_task'))
    elif datetime.strptime(exp_date1, '%Y-%m-%d').date() > datetime.strptime(exp_date2, '%Y-%m-%d').date():
        flash('Неправильные даты')
        return redirect(url_for('find_task'))

    cur.execute(f"SELECT * FROM TASK")
    table = cur.fetchall()
    conn.close()

    df = pd.DataFrame(
        {'ID задачи': [], 'Название': [], 'ID исполнителя': [], 'Срок исполнения': [], 'ID документа': []})
    for i in range(len(table)):
        if datetime.strptime(exp_date1, '%Y-%m-%d').date() <= datetime.strptime(table[i][3], '%Y-%m-%d').date() and datetime.strptime(exp_date2, '%Y-%m-%d').date() >= datetime.strptime(table[i][3], '%Y-%m-%d').date():
            df.loc[len(df.index)] = [table[i][0], table[i][1], table[i][2], table[i][3], table[i][4]]

    df = df.sort_values('ID задачи')

    return render_template('task.html', df=df)

@app.route('/find_doc')
def find_doc():
    return render_template("find_doc.html")

@app.route('/find_doc', methods =["POST"])
def find_docc():
    exp_date = request.form.get('exp_date')
    conn = psycopg2.connect(user="postgres", password="1234", host="127.0.0.1", port="5432", database="pbz_2")
    cur = conn.cursor()

    if exp_date == '':
        flash('Введите дату')
        return redirect(url_for('find_task'))

    cur.execute(f"SELECT TASK.ID, TASK.EXPLORER_ID, TASK.EXP_DATE, DOCUMENT.ID, DOCUMENT.RESOLUTION_ID, DOCUMENT.CONTROLLER_ID FROM TASK "
                f"JOIN DOCUMENT ON TASK.DOC_ID = DOCUMENT.ID")
    table = cur.fetchall()
    conn.close()

    df = pd.DataFrame(
        {'ID задачи': [], 'ID исполнителя': [], 'Срок исполнения': [], 'ID документа': [], 'ID резолюции': [], 'ID контролера': []})
    for i in range(len(table)):
        if datetime.strptime(exp_date, '%Y-%m-%d').date() >= datetime.strptime(table[i][2], '%Y-%m-%d').date():
            df.loc[len(df.index)] = [table[i][0], table[i][1], table[i][2], table[i][3], table[i][4], table[i][5]]

    df = df.sort_values('ID документа')

    return render_template('document.html', df=df)


if __name__== "__main__":
    app.run(debug=True)
