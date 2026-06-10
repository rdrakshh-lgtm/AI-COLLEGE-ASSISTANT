from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('chatbot.html')


@app.route('/chat', methods=['POST'])
def chat():

    data = request.get_json()
    user_message = data['message'].lower()

    # Attendance
    if "attendance" in user_message:
        reply = """
        Your current attendance is 85%.
        You need 75% minimum attendance to appear for exams.
        """

    # Timetable
    elif "timetable" in user_message:
        reply = """
        Today's Classes:
        
        9:00 AM - Machine Learning
        10:00 AM - Blockchain Technology
        11:30 AM - Cloud Computing
        2:00 PM - Software Engineering
        """

    # Exams
    elif "exam" in user_message:
        reply = """
        Upcoming Internal Exams:

        Machine Learning - 15 June
        Blockchain - 17 June
        Cloud Computing - 20 June
        """

    # Placement
    elif "placement" in user_message:
        reply = """
        Upcoming Placement Drives:

        Infosys
        TCS
        Wipro
        Accenture

        Eligibility: CGPA above 6.5
        """

    # Syllabus
    elif "syllabus" in user_message:
        reply = """
        Available Subjects:

        Machine Learning
        Blockchain Technology
        Cloud Computing
        Big Data Analytics
        Software Engineering
        """

    # Greetings
    elif any(word in user_message for word in ["hi", "hello", "hey"]):
        reply = """
        Hello Student 👋

        I can help with:
        • Attendance
        • Timetable
        • Exams
        • Placements
        • Syllabus
        """

    # Help
    elif "help" in user_message:
        reply = """
        Try asking:

        ➤ Show attendance
        ➤ Show timetable
        ➤ Upcoming exams
        ➤ Placement details
        ➤ Show syllabus
        """

    else:
        reply = f"""
        You asked: "{user_message}"

        I'm still learning.
        Please ask about:

        • Attendance
        • Timetable
        • Exams
        • Placements
        • Syllabus
        """

    return jsonify({
        "reply": reply
    })


if __name__ == '__main__':
    app.run(debug=True)