# -*- coding: utf-8 -*-
import codecs
import pyodbc
from flask import Flask, jsonify, redirect, render_template, request, session, json

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

import base64
import hashlib
import hmac
import time
import math

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
    admin_username = request.args.get("adm-username")
    admin_password = request.args.get("adm-password")

    student_name = request.args.get("student-name")
    student_lastname = request.args.get("student-lastname")
    student_fathername = request.args.get("student-fathername")

    if(admin_password and admin_username):
        if(adminLogin(admin_username, admin_password, addSudent.__name__)):
            if(student_name and student_lastname and student_fathername):
                students_db_read = open('uploads/students.txt', 'r')
                sudents_count = 0
                for s_line in students_db_read:
                    sudents_count += 1

                students_db_write = codecs.open('uploads/students.txt', 'a', encoding="utf-8")
                students_db_write.writelines(str(sudents_count) + ":" + student_lastname + ":" + student_name + ":" + student_fathername + ":" + str(True) + "\n")

                students_db_write.close()
                students_db_read.close()

                print(addSudent.__name__ + " удачно!" + "\n")
                return "Ученик " + student_name + " был добавлен под индексом " + str(sudents_count), 200

            print(addSudent.__name__ + " не удачно!" + "\n")
            return "Err: Вы не указали имя, фамилию или отчество студента!", 400

    return "Err: Логин или пороль админа не совпадают или слишком частое подлючение!", 400

@app.route("/check-student", methods=["POST", "GET"])
def checkSudent():
    students_db_read = codecs.open('uploads/students.txt', 'r', encoding="utf-8")
    for s_line in students_db_read:
        return s_line

# adminLogin() func
# подключена antiSpam система!
# - проверяет доступ админа к управнию системы
# - выводит сообщения о попытке клиента, доступе и резутата проверки антиспам системы
def adminLogin(username, password, text):
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    print("\n" + "Клиент: " + client_ip)
    if(antiSpam.Check(client_ip)):
        antiSpam.Add(client_ip)
        print(Fore.CYAN + "\nПопытка входа админа: " + username + ":" + password + " с целью: '" + text + "'" + Style.RESET_ALL)

        if(username != "" and username and password != "" and password):
            admin_db = open('uploads/admins.txt', 'r')

            #Добавить юзабельность хэшеру!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            hasher = PSWHash256()
            
            for line in admin_db:
                user = line.split(':')
                if(user[0] == username): #хэшер здесь!
                    if(user[1] == password): #и здесь!
                        print(Fore.GREEN + "Успешный вход админа: " + username + Style.RESET_ALL )
                        admin_db.close()
                        return True
                    print(Fore.RED + "Не правильный пороль!" + Style.RESET_ALL)

    antiSpam.Add(client_ip)
    print(Fore.RED + "Внимание! Не успешный вход админа: " + username + Style.RESET_ALL + "\n")
    return False

#Система анти дудоса. 
# Проверяет делал ли пользователь недавно запрос. 
# Если он делал его < __loginsReload секунд назад, то не дает доступ и вывожит сообщение!
# !!! Инициализация не нужна
#
# Кста, реально кртая тема! Во так наглядно выглядит статический метод. У него статические параметры и методы
# !!! Все file read/write закрываються
class antiSpam:
    #private
    __loginsReload = 1
    __logs_path = 'uploads/anti-spam-system/logins.txt'

# Add(ip) func
# - при запросе сохраняет инфу о ip клиента и о времяни запроса в файл
    def Add(ip):
        login_db = open(antiSpam.__logs_path, 'a')
        login_db.writelines(ip + ":" + str(math.floor(time.time())) + "\n")
        login_db.close()

# Check(ip) func
# - при запросе проверяет недавнюю активность пользователя
# - если он делал запрос < __loginsReload секунд назад, то возвращает false и выводит сообщение!
# - в другом случае true
    def Check(ip):
        login_db = open(antiSpam.__logs_path, 'r')
        for line in login_db:
            logs = line.split(':')
            if(logs[0] == ip):
                if(time.time() - int(logs[1]) < antiSpam.__loginsReload):
                    login_db.close()
                    print(Fore.RED + "Слишком частое подлючение!" + Style.RESET_ALL)
                    return False
        login_db.close()
        return True