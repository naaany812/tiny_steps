from flask import Flask, render_template, request
import json
from random import sample

app = Flask(__name__)


def loads_json(path):
    with open(path, "r", encoding="utf8") as f:
        content = f.read()
        return json.loads(content)


def dumps_json(path, form):
    with open(path, "a+", encoding="utf8") as f:
        dumped_data = json.dumps(form)
        f.write(",\n")
        f.write(dumped_data)


goals_mock = loads_json(r"./data/goals.json")
teachers = loads_json(r"./data/teachers.json").get("teachers")
days = loads_json(r"./data/days.json")


@app.route("/")
def main():
    random_teachers = sample(teachers, k=6)
    return render_template("index.html", teachers=random_teachers)


@app.route("/goals/<goal>/")
def goals(goal):
    goal_value = goals_mock.get(goal)
    needed_teachers = list()
    t_params = ["id", "name", "about", "rating", "picture", "price", "goals"]
    for teacher in teachers:
        if goal in teacher.get("goals"):
            temp_teacher = dict()
            for t_id in t_params:
                temp_teacher[t_id] = teacher[t_id]
            needed_teachers.append(temp_teacher)
    return render_template(
        "goal.html",
        goal_value=goal_value,
        teachers=needed_teachers)


@app.route("/profiles/<int:teacher_id>/")
def profile(teacher_id):
    teacher = teachers[teacher_id]
    timesheet = teacher["free"]
    teacher_goals = ", ".join(goals_mock.get(g) for g in teacher.get("goals"))
    return render_template(
        "profile.html",
        teacher=teacher,
        goals=teacher_goals,
        timesheet=timesheet)


@app.route("/request/")
def send_request():
    return render_template("request.html")


@app.route("/request_done/", methods=["POST"])
def request_done():
    request_form = request.form
    goal = goals_mock.get(request_form.get("goal"))
    dumps_json(r"./data/request.json", request_form)
    return render_template(
        "request_done.html",
        request=request_form,
        goal=goal)


@app.route("/booking/<int:teacher_id>/<day>/<time>/")
def booking(teacher_id, day, time):
    teacher = teachers[teacher_id]
    selected_day = days.get(day)
    return render_template(
        "booking.html",
        teacher=teacher,
        day=selected_day,
        time=time)


@app.route("/booking_done/", methods=["POST"])
def booking_done():
    booking_info = request.form
    dumps_json(r"./data/booking.json", booking_info)
    return render_template("booking_done.html", info=booking_info)


if __name__ == '__main__':
    app.run()
