from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__ , template_folder="templates")

# Helper function to interact with the SQLite database
def query_database(query, params=()):
    conn = sqlite3.connect('chat_assistant.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.close()
    return result

# Query functions
def get_employees_by_department(department):
    query = "SELECT Name, Salary, Hire_Date FROM Employees WHERE Department = ?"
    return query_database(query, (department,))

def get_manager_of_department(department):
    query = "SELECT Manager FROM Departments WHERE Name = ?"
    return query_database(query, (department,))

def get_employees_hired_after(date):
    query = "SELECT Name, Department, Hire_Date FROM Employees WHERE Hire_Date > ?"
    return query_database(query, (date,))

def get_total_salary_expense(department):
    query = "SELECT SUM(Salary) FROM Employees WHERE Department = ?"
    result = query_database(query, (department,))
    return result[0][0] if result else 0

# Flask Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/query', methods=['GET'])
def handle_query():
    user_query = request.args.get('query', '').lower()
    response = ""
    
    if "employees in the" in user_query and "department" in user_query:
        department = user_query.split('in the')[1].split('department')[0].strip()
        employees = get_employees_by_department(department)
        response = f"Employees in {department}: {employees}"

    elif "manager of the" in user_query and "department" in user_query:
        department = user_query.split('manager of the')[1].split('department')[0].strip()
        manager = get_manager_of_department(department)
        response = f"The manager of {department} is {manager[0][0]}."

    elif "employees hired after" in user_query:
        date = user_query.split('after')[1].strip()
        employees = get_employees_hired_after(date)
        response = f"Employees hired after {date}: {employees}"

    elif "total salary expense for the" in user_query and "department" in user_query:
        department = user_query.split('for the')[1].split('department')[0].strip()
        total_salary = get_total_salary_expense(department)
        response = f"The total salary expense for {department} is ${total_salary}."
    
    else:
        response = "Sorry, I didn't understand your query."

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
