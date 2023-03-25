# -*- coding: utf-8 -*-
from website import Website
from students import Student
from groups import Group
from disciplines import Discipline

from flask import Flask, jsonify, redirect, render_template, request, session, json
from waitress import serve
import socket 

from transliterate import translit

app = Flask(__name__, static_url_path='/static')
website = Website("mywebsite")
UPLOAD_FOLDER = '/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.from_object(__name__)

app.secret_key = b'/*/6379&63#=-;fg'

#MAIN
#
@app.route('/routs',  methods=["GET"])
def routs():
    routs = ""
    for rule in app.url_map.iter_rules():
        routs += str(rule) + "\n"
    return routs

@app.route('/',  methods=["GET"])
def index():
    return website.admin.showInfo()

# POSTS routs
#
# Проверить с 19 марта
@app.route("/add-student", methods=["POST", "GET"])
def addStudent():
    group_id = request.args.get("group")
    student = Student(request.args.get("name"), 
                      request.args.get("lastname"), 
                      request.args.get("fathername"))
    if(website.admin.getClientStatus() in {"admin", "teacher"}):
        return website.post.addStudent(student, group_id)
    return jsonify(message="Вы не админ"), 400

#
# Проверить с 19 марта
@app.route("/add-group", methods=["POST", "GET"])
def addGroup():
    group = Group(request.args.get("speciality"), 
                  request.args.get("course"), 
                  request.args.get("number"))
    if(website.admin.getClientStatus() in {"admin", "teacher"}):
        return website.post.addGroup(group)
    return jsonify(message="Вы не админ"), 400

#
@app.route("/add-discipline", methods=["POST", "GET"])
def addDiscipline():
    if(website.admin.getClientStatus() in {"admin", "teacher"}):
        discipline = Discipline(request.args.get("name"))
        website.post.addDiscipline(discipline)
    return jsonify(message="Вы не админ"), 400

#
@app.route("/add-attendance", methods=["POST", "GET"])
def addAttendance():
    print(website.admin.getClientStatus())
    if(website.admin.getClientStatus() in {"admin", "teacher"}):
        website.post.addAttendance(request.args.get("student-id"), request.args.get("discipline"), request.args.get("time"))
    return jsonify(message="Вы не админ"), 400

#
@app.route("/login", methods=["POST", "GET"])
def Login():
    username = request.args.get("username")
    password = request.args.get("password")
    return website.admin.Login(username, password)

#
@app.route("/unlogin", methods=["POST", "GET"])
def adminUnlogin():
    website.admin.Unlogin()
    return jsonify(message="Вы вышли из профиля"), 201

# GETS routs
# http://127.0.0.1:5000/api/get-student-by-ids?group_index=%D0%B8%D1%81%D0%BF-372&student_index=0
# Проверить с 19 марта
@app.route("/api/get-student-by-ids", methods=["GET"])
def getStudent():
    if(website.admin.getClientStatus() in {"admin", "teacher", "student"}):
        return website.get.getStudentByGroupAndId(request.args.get("group-id"), request.args.get("student-id"))
    return jsonify(message="Вы не учитель"), 400

# Проверить с 19 марта
@app.route("/api/get-group", methods=["GET"])
def getGroup():
    if(website.admin.getClientStatus() in {"admin", "teacher", "student"}):
        return website.get.getGroupByName(request.args.get("group_name"))
    return jsonify(message="Вы не учитель или ученик"), 400
# 404
#
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify(message=str(e)), 404

if __name__ == '__main__':
    hostname = socket.gethostname()
    print(hostname)
    print("Ip: "+ str(socket.gethostbyname(hostname)))
    _port = 5000
    print("Port: " + str(_port))
    serve(app, port=_port, host="0.0.0.0")
    #flask run --host=0.0.0.0 -p 8080