# -*- coding: utf-8 -*-
import website
from flask import Flask, jsonify, redirect, render_template, request, session, json

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

import base64
import hashlib
import hmac

class PSWHash256:
    def getHash(self, passwrd):
        passwrd = str.encode(passwrd)
        hash_psw = hmac.new(app.secret_key, msg=passwrd, digestmod=hashlib.sha256).digest()
        return base64.b64encode(hash_psw).decode()

app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = '/uploads'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.from_object(__name__)

app.secret_key = b'/*/6379&63#=-;fg'

if __name__ == '__main__':
    app.run(port=80)

#MAIN
@app.route('/',  methods=["POST", "GET"])
def index():
    return "Its working!"

# addSudent() func
@app.route("/add-student", methods=["POST", "GET"])
def addSudent():
    student_name = request.args.get("student-name")
    student_lastname = request.args.get("student-lastname")
    student_fathername = request.args.get("student-fathername")

    if(website.adminCheck()):
        return website.addStudent(student_name, student_lastname, student_fathername)
    return "Err: Вы не админ или слишком частое подлючение!", 400

@app.route("/admin-login", methods=["POST", "GET"])
def adminLogin():
    admin_username = request.args.get("adm-username")
    admin_password = request.args.get("adm-password")
    if(website.adminLogin(admin_username, admin_password, adminLogin.__name__)):
        return "Теперь вы админ!", 501
    return "Не правильный логин или пороль!", 502

@app.route("/admin-unlogin", methods=["POST", "GET"])
def adminUnlogin():
    if(website.adminCheck()):
        website.adminUnloginAll()
        return "Вы больше не админ!", 503
    return "Err: Вы не админ или слишком частое подлючение!", 400