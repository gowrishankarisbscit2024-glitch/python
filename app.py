from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            empno INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            salary REAL NOT NULL,
            designation TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT empno, name, salary, designation FROM employees')
    employees = cursor.fetchall()
    conn.close()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['POST'])
def add_employee():
    empno = request.form['empno']
    name = request.form['name']
    salary = request.form['salary']
    designation = request.form['designation']
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO employees (empno, name, salary, designation) VALUES (?, ?, ?, ?)', (empno, name, salary, designation))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:empno>')
def edit_employee(empno):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT empno, name, salary, designation FROM employees WHERE empno = ?', (empno,))
    employee = cursor.fetchone()
    conn.close()
    return render_template('edit.html', employee=employee)

@app.route('/update/<int:empno>', methods=['POST'])
def update_employee(empno):
    name = request.form['name']
    salary = request.form['salary']
    designation = request.form['designation']
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE employees SET name = ?, salary = ?, designation = ? WHERE empno = ?', (name, salary, designation, empno))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:empno>')
def delete_employee(empno):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE empno = ?', (empno,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/salary/<int:empno>')
def get_employee_salary(empno):
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    cursor.execute('SELECT empno, name, salary, designation FROM employees WHERE empno = ?', (empno,))
    employee = cursor.fetchone()
    conn.close()
    if employee:
        empno, name, salary, designation = employee
        basic = salary
        hra = 0.2 * basic
        da = 0.1 * basic
        gross = basic + hra + da
        pf = 0.12 * basic
        net = gross - pf
        return render_template(
            'salary_slip.html',
            empno=empno,
            name=name,
            designation=designation,
            basic=basic,
            hra=hra,
            da=da,
            gross=gross,
            pf=pf,
            net=net
        )
    else:
        return f"Employee {empno} not found"

if __name__ == '__main__':
    app.run(debug=True)
