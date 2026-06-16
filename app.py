# Chatbot Page
import google.generativeai as genai
import fitz




from flask import Flask, render_template, request, redirect, session, jsonify
from database import db, cursor

genai.configure(api_key="key")
for m in genai.list_models():
    print(m.name)

model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)
app.secret_key = "collegeassistant123"


import os

UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

import os

app.config['UPLOAD_FOLDER'] = r'C:\Users\rdrak\OneDrive\Desktop\college chatbot\uploads'

# Home Page
@app.route('/')
def home():
    return redirect('/login')


# Register Page
@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        sql = """
        INSERT INTO students(name, email, password)
        VALUES(%s, %s, %s)
        """

        values = (name, email, password)

        cursor.execute(sql, values)
        db.commit()

        return redirect('/login')

    return render_template('register.html')


# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cursor.execute(
            "SELECT * FROM students WHERE email=%s AND password=%s",
            (email, password)
        )

        user = cursor.fetchone()

        if user:

            session['user_id'] = user[0]
            session['name'] = user[1]
            session['email'] = user[2]

            return redirect('/dashboard')

        return "Invalid Email or Password"

    return render_template('login.html')

@app.route('/chatbot')
def chatbot():

    if 'user_id' not in session:
        return redirect('/login')

    return render_template(
        'chatbot.html',
        name=session['name']
    )


@app.route('/attendance')
def attendance():

    if 'user_id' not in session:
        return redirect('/login')

    cursor.execute(
        "SELECT percentage FROM attendance WHERE student_id=%s",
        (session['user_id'],)
    )

    result = cursor.fetchone()

    if result:
        attendance_percentage = float(result[0])
    else:
        attendance_percentage = 0

    return render_template(
        'attendance.html',
        name=session['name'],
        attendance=attendance_percentage
    )


# Dashboard
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        return redirect('/login')

    student_id = session['user_id']

    cursor.execute(
        "SELECT percentage FROM attendance WHERE student_id=%s",
        (student_id,)
    )

    attendance = cursor.fetchone()

    return render_template(
        'dashboard.html',
        name=session['name'],
        attendance=attendance[0]
    )


# Test Route
@app.route('/test')
def test():

    return str(session)





def read_all_pdfs():

    text = ""

    for filename in os.listdir(app.config['UPLOAD_FOLDER']):

        if filename.endswith(".pdf"):

            pdf_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                filename
            )

            doc = fitz.open(pdf_path)

            for page in doc:
                text += page.get_text()

    return text

pdf_text = read_all_pdfs()

@app.route('/chat', methods=['POST'])
def chat():

    data = request.get_json()
    user_message = data['message']

    # Read latest PDFs every time
    pdf_text = read_all_pdfs()

    # Get placement data
    cursor.execute("""
        SELECT company_name,
               role_name,
               package,
               eligibility
        FROM placements
    """)

    placements = cursor.fetchall()

    placement_text = ""

    for p in placements:

        placement_text += f"""
Company: {p[0]}
Role: {p[1]}
Package: {p[2]}
Eligibility: {p[3]}

"""

    try:

        prompt = f"""
You are an AI College Assistant.

You help students with:

1. Study materials and syllabus.
2. Placement opportunities.
3. Company eligibility.
4. Career guidance.

Placement Information:
{placement_text}

Study Material:
{pdf_text[:50000]}

Student Question:
{user_message}

Give clear and student-friendly answers.
"""

        response = model.generate_content(prompt)

        return jsonify({
            "reply": response.text
        })

    except Exception as e:

        return jsonify({
            "reply": f"Error: {str(e)}"
        })

# Logout
@app.route('/logout')
def logout():

    session.clear()

    return redirect('/login')

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():

    file = request.files['pdf']

    if file.filename == '':
        return "No file selected"

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        file.filename
    )

    print("Saving to:", os.path.abspath(filepath))

    file.save(filepath)

    return "PDF Uploaded Successfully"



  

@app.route('/files')
def files():
    pdfs = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(pdfs)





@app.route('/timetable')
def timetable():

    if 'user_id' not in session:
        return redirect('/login')

    cursor.execute("SELECT * FROM weekly_timetable_new")

    timetable_data = cursor.fetchall()

    print("Timetable Data:", timetable_data)

    return render_template(
        'timetable.html',
        timetable=timetable_data
    )


import os

@app.route('/syllabus')
def syllabus():

    files = os.listdir(app.config['UPLOAD_FOLDER'])

    return render_template(
        'syllabus.html',
        files=files
    )
from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
   return send_from_directory(
    app.config['UPLOAD_FOLDER'],
    filename
)

@app.route('/placements')
def placements():

    if 'user_id' not in session:
        return redirect('/login')

    cursor.execute("SELECT * FROM placements")
    placement_data = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM placements")
    total_companies = cursor.fetchone()[0]

    return render_template(
        'placements.html',
        placements=placement_data,
        total_companies=total_companies,
        name=session['name']
    )

@app.route('/resume')
def resume():

    if 'user_id' not in session:
        return redirect('/login')

    return render_template('resume.html')

@app.route('/upload_resume', methods=['POST'])
def upload_resume():

    if 'user_id' not in session:
        return redirect('/login')

    file = request.files['resume']

    if file.filename == '':
        return "No file selected"

    filepath = os.path.join(
        app.config['UPLOAD_FOLDER'],
        file.filename
    )

    file.save(filepath)

    cursor.execute(
        """
        INSERT INTO resumes(student_id, resume_file)
        VALUES(%s,%s)
        """,
        (session['user_id'], file.filename)
    )

    db.commit()

    return "Resume Uploaded Successfully"
# Run App
if __name__ == '__main__':
    app.run(debug=True)
