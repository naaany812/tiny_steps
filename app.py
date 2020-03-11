from flask import Flask, render_template, request
from random import sample
from models import db, Teacher, Study_Request, Booking
from enums import Goals, Days
from forms import Booking_form, Request_form

app = Flask(__name__)
app.secret_key = 'It is my cat! My cat is fat'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)


@app.route("/")
def main():
    teachers = db.session.query(Teacher).all()
    random_teachers = sample(teachers, k=6)
    return render_template("index.html", teachers=random_teachers)


@app.route("/goals/<goal>/")
def goals(goal):
    teachers = db.session.query(Teacher).all()
    goal_value = Goals[goal].value
    needed_teachers = list()
    for teacher in teachers:
        if goal in teacher.goals:
            needed_teachers.append(teacher)
    return render_template(
        "goal.html",
        goal_value=goal_value,
        teachers=needed_teachers)


@app.route("/profiles/<int:teacher_id>/")
def profile(teacher_id):
    teacher = db.session.query(Teacher).get_or_404(teacher_id)
    timesheet = teacher.free
    teacher_goals = ", ".join(Goals[g].value for g in teacher.goals)
    return render_template(
        "profile.html",
        teacher=teacher,
        goals=teacher_goals,
        timesheet=timesheet)


@app.route("/request/")
def send_request():
    request_form = Request_form()
    return render_template("request.html", form=request_form)


@app.route("/request_done/", methods=["POST"])
def request_done():
    request_form = Request_form(request.form)
    goal = Goals[request_form.goal.data].value
    if request_form.validate_on_submit():
        study_Request = Study_Request(
            goal=goal,
            time=request_form.time.data,
            name=request_form.name.data,
            phone=request_form.phone.data)
        db.session.add(study_Request)
        db.session.commit()
    return render_template(
        "request_done.html",
        form=request_form,
        goal=goal)


@app.route("/booking/<int:teacher_id>/<day>/<time>/")
def booking(teacher_id, day, time):
    teacher = db.session.query(Teacher).get(teacher_id)
    selected_day = Days[day].value
    booking_form = Booking_form()
    return render_template(
        "booking.html",
        teacher=teacher,
        day=selected_day,
        time=time,
        form=booking_form)


@app.route("/booking_done/", methods=["POST"])
def booking_done():
    booking_info = Booking_form(request.form)
    if booking_info.validate_on_submit():
        booking = Booking(
            name=booking_info.name.data,
            phone=booking_info.phone.data,
            day=booking_info.day.data,
            time=booking_info.time.data,
            teacher_id=booking_info.teacher_id.data
        )
        db.session.add(booking)
        db.session.commit()
    return render_template("booking_done.html", info=booking_info)


if __name__ == '__main__':
    app.run()
