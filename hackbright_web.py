"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    return render_template('student_info.html', github=github,
                           first=first, last=last)


@app.route("/new-student-form")
def add_student_form():
    """Show form for searching student"""

    return render_template("new_student.html")


@app.route("/student-add", methods=['POST'])
def display_new_student():
    """Show information about a new student."""

    github = request.form.get('github')
    first = request.form.get('first')
    last = request.form.get('last')

    hackbright.make_new_student(first, last, github)

    return render_template('new_student_confirmation.html', github=github)


@app.route("/student-search")
def get_student_form():
    """Show form for searching student"""

    return render_template("student_search.html")


if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
