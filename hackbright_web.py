"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect

import hackbright

app = Flask(__name__)


@app.route('/')
def show_homepage():
    """Homepage for the student projects"""

    students = hackbright.show_all_students()
    projects = hackbright.show_all_projects()

    return render_template('homepage.html', students=students, projects=projects)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    rows = hackbright.get_grades_by_github(github)

    return render_template('student_info.html', github=github,
                           first=first, last=last, rows=rows)


@app.route("/student-add")
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


@app.route("/project")
def display_project():
    """Show project for given title"""

    title = request.args.get('title')

    row = hackbright.get_project_by_title(title)
    grades_rows = hackbright.get_grades_by_title(title)

    return render_template("project.html", row=row, grades_rows=grades_rows)


@app.route("/project-add")
def add_project_form():
    """Show form for adding new project"""

    return render_template("add_project.html")


@app.route("/project_add", methods=['POST'])
def display_project_form():
    """Show new project form"""

    title = request.form.get('title')
    description = request.form.get('description')
    max_grade = request.form.get('max_grade')

    hackbright.add_project(title, description, max_grade)

    return render_template('project_confirmation_page.html', title=title)


@app.route("/assign-grade")
def show_student_grade_form():
    """Show form for assigning student grade"""

    students = hackbright.show_all_students()
    projects = hackbright.show_all_projects()

    return render_template("assign_grade.html", students=students, projects=projects)


@app.route("/assign-grade", methods=['POST'])
def assign_student_grade():
    """Update database with student grade on project"""

    student = request.form.get('student')
    project = request.form.get('project')
    grade = request.form.get('grade')

    if hackbright.get_grade_by_github_title(student, project) is not None:
        hackbright.update_grade(student, project, grade)

    else:
        hackbright.assign_grade(student, project, grade)

    return redirect('/student?github={student}'.format(student=student))



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
