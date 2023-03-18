# -*- coding: utf-8 -*-
from website import Website
from students import Student
from groups import Group
from disciplines import Discipline

from flask import Flask, jsonify, redirect, render_template, request, session, json


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
    return website.admin.checkLogin()

# POSTS routs
#
@app.route("/add-student", methods=["POST", "GET"])
def addStudent():
    group_id = request.args.get("group")
    student = Student(request.args.get("name"), request.args.get("lastname"), request.args.get("fathername"))
    if(website.admin.adminCheck()):
        return website.post.addStudent(student, group_id)
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
@app.route("/login", methods=["POST", "GET"])
def adminLogin():
    admin_username = request.args.get("username")
    admin_password = request.args.get("password")
    return website.admin.adminLogin(admin_username, admin_password)

#
@app.route("/unlogin", methods=["POST", "GET"])
def adminUnlogin():
    if(website.admin.adminCheck()):
        website.admin.adminUnloginAll()
        return "Вы больше не админ", 200
    return "Вы и так не админ", 200
# GETS routs

# http://127.0.0.1:5000/api/get-student-by-ids?group_index=%D0%B8%D1%81%D0%BF-372&student_index=0
@app.route("/api/get-student-by-ids", methods=["GET"])
def getStudent():
    group_id = request.args.get("group_index")
    student_index = request.args.get("student_index")
    if(website.admin.adminCheck()):
        return website.get.getStudentByGroupAndIndex(group_id, student_index)
    return "Err: Вы не админ или слишком частое подлючение!", 400

@app.route("/api/get-group", methods=["GET"])
def getGroup():
    if(website.admin.adminCheck()):
        return website.get.getGroupByName(request.args.get("group_name"))
    return "Err: Вы не админ или слишком частое подлючение!", 400
# 404
#
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify(error=str(e)), 404