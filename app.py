from flask import Flask, render_template, request
from json import loads, dumps
from random import sample

app = Flask(__name__)

goals_mock = dict()
with open(r"data/goals.json", "r", encoding="utf8") as f:
    content = f.read()
    goals_mock = loads(content)


teachers = []
with open(r"data/teachers.json", "r", encoding="utf8") as f:
    contents = f.read()
    teachers = loads(contents).get("teachers")


days = dict()
with open(r"data/days.json", "r", encoding="utf8") as f:
    content = f.read()
    days = loads(content)


@app.route("/")
def main():
    random_teachers = sample(teachers, k=6)
    return render_template("index.html",
    teachers=random_teachers)


@app.route("/goals/<goal>/")
def goals(goal):
    goal_value = goals_mock.get(goal)
    needed_teachers = list()
    for teacher in teachers:
        if goal in teacher.get("goals"):
            temp_teacher = dict()
            for t_id in ["id", "name", "about", "rating", "picture", "price", "goals"]:
                temp_teacher[t_id] = teacher[t_id]
            needed_teachers.append(temp_teacher)
    return render_template("goal.html", 
    goal_value=goal_value,
    teachers=needed_teachers)


@app.route("/profiles/<int:teacher_id>/")
def profile(teacher_id):
    teacher = teachers[teacher_id]
    timesheet = teacher["free"]
    teacher_goals=", ".join(goals_mock.get(g) for g in teacher.get("goals"))
    return render_template("profile.html",
    teacher = teacher,
    goals = teacher_goals,
    timesheet = timesheet)


@app.route("/request/")
def send_request():
    return render_template("request.html")


@app.route("/request_done/", methods=["POST"])
def request_done():
    request_form = request.form
    goal = goals_mock.get(request_form.get("goal"))
    with open(r"data/request.json", "a+", encoding="utf8") as f:
        request_dumped = dumps(request_form)
        f.write(",\n")
        f.write(request_dumped)    
    return render_template("request_done.html",
    request=request_form,
    goal=goal)


@app.route("/booking/<int:teacher_id>/<day>/<time>/")
def booking(teacher_id, day, time):
    teacher = teachers[teacher_id]
    selected_day=days.get(day)
    return render_template("booking.html",
    teacher=teacher,
    day=selected_day,
    time=time)


@app.route("/booking_done/", methods=["POST"])
def booking_done():
    booking_info = request.form
    with open(r"data/booking.json", "a+", encoding="utf8") as f:
        booking_dumped = dumps(booking_info)
        f.write(",\n")
        f.write(booking_dumped)
    return render_template("booking_done.html",
    info=booking_info)


if __name__ == '__main__':
    app.run()

