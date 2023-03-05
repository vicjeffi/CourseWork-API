# -*- coding: utf-8 -*-
from website import Website
from students import Student
from groups import Group

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
@app.route('/',  methods=["GET"])
def index():
    if(website.admin.adminCheck()):
        return "Вы админ!"
    return "Its working!"

# POSTS routs
@app.route("/add-student", methods=["POST", "GET"])
def addStudent():
    group_id = request.args.get("group")
    student = Student(request.args.get("student-name"), request.args.get("student-lastname"), request.args.get("student-fathername"))
    if(website.admin.adminCheck()):
        return website.post.addStudent(student, group_id.lower())
    return "Err: Вы не админ или слишком частое подлючение!", 400

@app.route("/add-group", methods=["POST", "GET"])
def addGroup():
    group = Group(request.args.get("speciality"), request.args.get("course"), request.args.get("number"))
    if(website.admin.adminCheck()):
        return website.post.addGroup(group)
    return "Err: Вы не админ или слишком частое подлючение!", 400

# ADMINS logins routs
@app.route("/admin-login", methods=["POST", "GET"])
def adminLogin():
    admin_username = request.args.get("adm-username")
    admin_password = request.args.get("adm-password")
    if(website.adminLogin(admin_username, admin_password, adminLogin.__name__)):
        return "Теперь вы админ!", 501
    return "Не правильный логин или пороль!", 502

@app.route("/admin-unlogin", methods=["POST", "GET"])
def adminUnlogin():
    if(website.admin.adminCheck()):
        website.admin.adminUnloginAll()
        return "Вы больше не админ!", 503
    return "Err: Вы не админ или слишком частое подлючение!", 400
