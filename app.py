# -*- coding: utf-8 -*-
from website import Website
from students import Student
from groups import Group
from disciplines import Discipline

from flask import Flask, jsonify, request, json
from waitress import serve
import socket 


###                                  ###
###            1) CONFIG:            ###
###                                  ###

app = Flask(__name__, static_url_path='/static')
website = Website("mywebsite")
UPLOAD_FOLDER = '/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.from_object(__name__)

app.secret_key = b'/*/6379&63#=-;fg'

###                                  ###
###        2) ALL MAIN ROUTS:        ###
###                                  ###

# RUN CONFIG
# flask run --host=0.0.0.0 -p 8080
if __name__ == '__main__':
    hostname = socket.gethostname()
    print(hostname)
    print("Ip: "+ str(socket.gethostbyname(hostname)))
    _port = 5000
    print("Port: " + str(_port))
    serve(app, port=_port, host="0.0.0.0")

# TEST!
@app.route('/routs',  methods=["GET"])
def routs():
    routs = ""
    for rule in app.url_map.iter_rules():
        routs += str(rule) + "\n"
    return routs

# CLIENT! ALL!
@app.route('/',  methods=["GET"])
def index():
    return website.admin.showInfo()

###                                  ###
###            2.1) POSTS            ###
###                                  ###

# ADMIN!
# Проверить с 19 марта
@app.route("/add-user", methods=["POST", "GET"])
def addUser():
    if(website.admin.getClientStatus() in {"admin", "teacher"}):
        group_id = request.args.get("group")
        student = Student(request.args.get("name"), 
                      request.args.get("lastname"), 
                      request.args.get("fathername"))
        return website.post.addStudent(student, group_id)
    return jsonify(message="Вы не админ"), 400

# ADMIN!
@app.route("/add-student", methods=["POST", "GET"])
def addStudent():
    if(website.admin.getClientStatus() in {"admin", "teacher"}):
        group_id = request.args.get("group")
        student = Student(request.args.get("name"), 
                      request.args.get("lastname"), 
                      request.args.get("fathername"))
        return website.post.addStudent(student, group_id)
    return jsonify(message="Вы не админ"), 400

# TEST!
# GET RANDOM ID
@app.route("/test", methods=["POST", "GET"])
def test():
    return Student.getRandomId()

# TEST!
@app.route("/test6", methods=["POST", "GET"])
def test6():
    student1 = Student("Vic", "Jeff", "Methon")
    student2 = Student("Heron", "Lite", "Billirson")
    myDict = {'Student': [{'id': student1.id, 'firstname': student1.firstname, 'lastname': student1.lastname, 'fathername': student1.fathername}]}
    myDict['Student'].append(({'id': student2.id, 'firstname': student2.firstname, 'lastname': student2.lastname, 'fathername': student2.fathername}))
    test = json.dumps(myDict,sort_keys=False)
    return test, 200

# ADMIN!
# Проверить с 19 марта
@app.route("/add-group", methods=["POST", "GET"])
def addGroup():
    group = Group(request.args.get("speciality"), 
                  request.args.get("course"), 
                  request.args.get("number"))
    if(website.admin.getClientStatus() in {"admin", "teacher"}):
        return website.post.addGroup(group)
    return jsonify(message="Вы не админ"), 400

# ADMIN!
@app.route("/add-discipline", methods=["POST", "GET"])
def addDiscipline():
    if(website.admin.getClientStatus() in {"admin", "teacher"}):
        discipline = Discipline(request.args.get("name"))
        website.post.addDiscipline(discipline)
    return jsonify(message="Вы не админ"), 400

# ADMIN!
@app.route("/add-attendance", methods=["POST", "GET"])
def addAttendance():
    if(website.admin.getClientStatus() in {"admin", "teacher"}):
        website.post.addAttendance(request.args.get("student-id"), request.args.get("discipline"), request.args.get("time"))
    return jsonify(message="Вы не админ"), 400

# CLIENT!
@app.route("/login", methods=["POST", "GET"])
def Login():
    username = request.args.get("username")
    password = request.args.get("password")
    return website.admin.Login(username, password)

# CLIENT!
@app.route("/unlogin", methods=["POST", "GET"])
def adminUnlogin():
    website.admin.Unlogin()
    return jsonify(message="Вы вышли из профиля"), 201

###                                  ###
###              2.2 GETS:           ###
###                                  ###

# CLIENT!
# https://json2csharp.com/ - ДЛЯ C#
# http://json.parser.online.fr/ - ДЕКОДЕР ДЛЯ РУСКОГО ЯЗЫКА
@app.route("/api/get-students-by-group", methods=["GET"])
def getStudents():
    if(website.admin.getClientStatus() in {"admin", "teacher"}):
        return website.get.getStudentsByGroup(request.args.get("group-id"))
    return jsonify(message="Вы не учитель"), 400

#CLIENT!
@app.route("/api/get-user-by-ids", methods=["GET"])
def getUser():
    if(website.admin.getClientStatus() in {"admin", "teacher", "student"}):
        return website.get.getUserById(request.args.get("student-id"))
    return jsonify(message="Вы не вошли в профиль"), 400

# ПЕРЕДЕЛАТЬ НАФРЕН
@app.route("/api/get-group", methods=["GET"])
def getGroup():
    if(website.admin.getClientStatus() in {"admin", "teacher", "student"}):
        return website.get.getGroupByName(request.args.get("group_name"))
    return jsonify(message="Вы не учитель или ученик"), 400

# CLIENT!
@app.route("/api/my-data", methods=["GET"])
def getMyData():
    if(website.admin.getClientStatus() in {"admin", "teacher", "student"}):
        return website.get.getUserById(website.admin.getClientId())
    return jsonify(message="Вы не вошли в профиль"), 400

###                                  ###
###            2.3) UPLOADS:         ###
###                                  ###

# ... в будующем ...

###                                  ###
###            3) OTHERS:            ###
###                                  ###

# ALL!
@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return jsonify(message=str(e)), 404