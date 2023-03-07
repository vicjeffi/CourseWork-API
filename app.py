# -*- coding: utf-8 -*-
from website import Website
from students import Student
from groups import Group
from discipline import Discipline

from flask import Flask, jsonify, redirect, render_template, request, session, json

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

app = Flask(__name__, static_url_path='/static')
website = Website("MyWebsite")
UPLOAD_FOLDER = '/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.from_object(__name__)

app.secret_key = b'/*/6379&63#=-;fg'

if __name__ == '__main__':
    app.run(port=80)

#MAIN
#
@app.route('/',  methods=["GET"])
def index():
    if(website.admin.adminCheck()):
        return "Вы админ!"
    return "Its working!"

# POSTS routs
#
@app.route("/add-student", methods=["POST", "GET"])
def addStudent():
    group_id = request.args.get("group")
    student = Student(request.args.get("name"), request.args.get("lastname"), request.args.get("fathername"))
    if(website.admin.adminCheck()):
        return website.post.addStudent(student, group_id.lower())
    return "Err: Вы не админ или слишком частое подлючение!", 400

#
@app.route("/add-group", methods=["POST", "GET"])
def addGroup():
    group = Group(request.args.get("speciality"), request.args.get("course"), request.args.get("number"))
    if(website.admin.adminCheck()):
        return website.post.addGroup(group)
    return "Err: Вы не админ или слишком частое подлючение!", 400

@app.route("/add-discipline", methods=["POST", "GET"])
def addDiscipline():
    if(website.admin.adminCheck()):
        discipline = Discipline(request.args.get("name"))
        website.post.addDiscipline(discipline)
    return "Err: Вы не админ или слишком частое подлючение!", 400

# ADMINS logins routs
#
@app.route("/admin-login", methods=["POST", "GET"])
def adminLogin():
    admin_username = request.args.get("username")
    admin_password = request.args.get("password")
    if(website.adminLogin(admin_username, admin_password, adminLogin.__name__)):
        return "Теперь вы админ!", 501
    return "Не правильный логин или пороль!", 502

#
@app.route("/admin-unlogin", methods=["POST", "GET"])
def adminUnlogin():
    if(website.admin.adminCheck()):
        website.admin.adminUnloginAll()
        return "Вы больше не админ!", 503
    return "Err: Вы не админ или слишком частое подлючение!", 400
# GETS routs

#
@app.route("/get-student-by-ids", methods=["GET"])
def getStudent():
    group_id = request.args.get("group_index")
    student_index = request.args.get("student_index")
    if(website.admin.adminCheck()):
        return website.get.getStudentByGroupAndIndex(group_id.lower(), student_index)
    return "Err: Вы не админ или слишком частое подлючение!", 400

# 404
#
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify(error=str(e)), 404