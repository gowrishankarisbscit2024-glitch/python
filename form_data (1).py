from flask import Flask, request, render_template, redirect

app = Flask(__name__)

# In-memory employee list
employees = []


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        empno = request.form['empno']
        name = request.form['name']
        salary = request.form['salary']
        designation = request.form['designation']

        employees.append({
            'empno': empno,
            'name': name,
            'salary': salary,
            'designation': designation
        })

        return redirect('/')

    return render_template('index.html', employees=employees)


if __name__ == '__main__':
    app.run(debug=True)
