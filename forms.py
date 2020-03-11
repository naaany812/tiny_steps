from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, RadioField
from wtforms.validators import DataRequired


class Booking_form(FlaskForm):
    name = StringField(
        'Вас зовут',
        validators=[DataRequired()])
    phone = StringField(
        'Ваш телефон',
        validators=[DataRequired()])
    day = StringField('day')
    time = StringField('time')
    teacher_id = IntegerField('teacher_id')


class Request_form(FlaskForm):
    goal = RadioField(
        'Какая цель занятий?',
        default="travel",
        choices=[
            ("travel", "Для путешествий"),
            ("study", "Для школы"),
            ("work", "Для работы"),
            ("relocate", "Для переезда")])

    time = RadioField(
        'Сколько времени есть?',
        default="1-2",
        choices=[
            ("1-2", "1-2 часа в&nbsp;неделю"),
            ("3-5", "3-5 часов в&nbsp;неделю"),
            ("5-7", "5-7 часов в&nbsp;неделю"),
            ("7-10", "7-10 часов в&nbsp;неделю")])

    name = StringField(
        'Вас зовут',
        validators=[DataRequired()])

    phone = StringField(
        'Ваш телефон',
        validators=[DataRequired()])
