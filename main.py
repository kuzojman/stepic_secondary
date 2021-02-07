from flask import Flask, request, render_template
from wtforms.validators import InputRequired, Email
from flask_wtf import FlaskForm
from wtforms import StringField,RadioField
from data import teachers, goals,day_in_week_dictionary
import random
import json


data_to_json = [{"name":"A",
                "phone":"B",
                "trainer":"C",
                "radio_field_week":"D"}]

##data_to_json_2 = [ {"name":"A","phone":"B","trainer":"C", "radio_field_week":"D"},{"name":"B","phone":"C","trainer":"D","radio_field_week":"E"}]

#####data_to_json.append(data_to_json_2)





app = Flask(__name__)
app.secret_key = "randomstring"


class MyForm(FlaskForm):
    trainer = RadioField('trainer', choices=[("Для путешествий", "Для путешествий"),
                                             ("Для школы", "Для школы"),
                                             ("Для работы", "Для работы"),
                                             ("Для переезда", "Для переезда"),])

    radio_field_week = RadioField('radio_field_week', choices=[("1-2 часа в неделю", "1-2 часа в неделю"),
                                                               ("3-5 часа в неделю", "3-5 часа в неделю"),
                                                               ("6-7 часа в неделю", "6-7 часа в неделю"),
                                                               ("8-10 часа в неделю", "8-10 часа в неделю")])

    name  = StringField('name',  [InputRequired()])
    phone = StringField('phone', [InputRequired()])








@app.route('/all')
def render_all():
    return render_template("all.html",
                           teachers=teachers)

@app.route('/booking/<number>/<day_in_week>/<time_to_study>')
def render_booking(number,day_in_week,time_to_study):
    form = MyForm()
    return render_template("booking.html",
                           teachers=teachers[int(number)],
                           day_in_week_dictionary=day_in_week_dictionary[day_in_week],
                           time_to_study=time_to_study,
                           form=form
                           )

@app.route('/booking_done/<day_in_week>/<time_to_study>',methods=["POST"])
def render_booking_done(day_in_week,time_to_study):
    form  = MyForm()
    name  = form.name.data
    phone = form.phone.data
    data_to_json_2 = [{"name":name,
                       "phone": phone,
                       "day_in_week":day_in_week,
                       "radio_field_week":time_to_study}]
    data_to_json.append(data_to_json_2)
    with open('result.json', 'w') as fp:
        json.dump(data_to_json, fp)

    return render_template("booking_done.html",
                           time_to_study=time_to_study,
                           day_in_week=day_in_week,
                           name=name,
                           phone=phone)





@app.route('/goal/<purpose>/')
def render_goal(purpose):
    teachers_2 = [t for t in teachers if purpose in t["goals"]]
    goal_to_study = goals[purpose]
    return render_template("goal.html",
                           teachers=teachers_2,
                           goal_to_study=goal_to_study,
                           goals=goals)

@app.route('/')
def render_index():
    teachers_3 = random.sample(teachers,6)
    return render_template("index.html",
                           teachers = teachers_3)


@app.route('/profile/<number>')
def render_profile(number):
    return render_template("profile.html",
                           teachers=teachers[int(number)],
                           goals=goals)



@app.route('/request')
def render_request():
    form  = MyForm()
    return render_template("request.html",
                           form=form)



@app.route('/request_done',methods=["POST"])
def render_request_done():
    form  = MyForm()
    name  = form.name.data
    phone = form.phone.data
    trainer = form.trainer.data
    radio_field_week =form.radio_field_week.data
    data_to_json_2 = [{"name":name,
                       "phone": phone,
                       "trainer":trainer,
                       "radio_field_week":radio_field_week}]
    data_to_json.append(data_to_json_2)
    with open('result.json', 'w') as fp:
        json.dump(data_to_json, fp)
    return render_template("request_done.html",
                           form=form,
                           name=name,
                           phone=phone,
                           trainer =trainer,
                           radio_field_week =radio_field_week)



if __name__ == '__main__':
    app.run()