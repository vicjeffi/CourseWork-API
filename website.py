from antispam import antiSpam
from students import Student
from groups import Group
from teachers import Teacher
from disciplines import Discipline

from flask import request, jsonify, json
import codecs

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

import secrets
import string
import datetime
import requests

from dotenv import dotenv_values

from transliterate import translit

alphabet = string.ascii_letters + string.digits
class Website:
    name = ""
    uploads =  "uploads" #"mysite/uploads"
    secrets = dotenv_values("mysite/" + ".env")
    onesignal_url = "https://onesignal.com/api/v1/notifications"
    def __init__(self, name : str):
        self.name = name
        self.post = self.Post()
        self.get = self.Get()
        self.admin = self.Admin()
        self.upload = self.Upload()
        print(Fore.CYAN + "Starting server, master!" + Style.RESET_ALL)

    class Admin:
        #ALl!
        def getClientId(self):
            if(not self.getIsClientLogined()):
                return "None"
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            logins = codecs.open(Website.uploads + '/login.txt', 'r', encoding="utf-8")
            for line in logins:
                lines = line.split(':')
                if(lines[0] == client_ip):
                    logins.close()
                    return lines[2]
            logins.close()

        # ALL!
        def getClientStatus(self):
            if(not self.getIsClientLogined()):
                return "None"
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            logins = codecs.open(Website.uploads + '/login.txt', 'r', encoding="utf-8")
            for line in logins:
                lines = line.split(':')
                if(lines[0] == client_ip):
                    logins.close()
                    return lines[1]
            logins.close()

        # ALL!
        def getIsClientLogined(self):
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            logins = codecs.open(Website.uploads + '/login.txt', 'r', encoding="utf-8")
            for line in logins:
                lines = line.split(':')
                if(lines[0] == client_ip):
                    logins.close()
                    return True
            logins.close()
            return False

        # ALL!
        def showInfo(self):
            return jsonify(
                logined = self.getIsClientLogined(),
                status = self.getClientStatus(),
                ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr),
                id = self.getClientId()
            )

        # CLIENT!
        def Unlogin(self, ip = ""):
            if(ip == ""):
                ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            with codecs.open(Website.uploads + '/login.txt', 'r', encoding='utf-8') as file:
                data = file.readlines()

            for index, line in enumerate(data):
                data[index] = line.strip() + "\n"
                cutLines = line.split(":")
                if (cutLines[0] == ip):
                    newLine = ""
                    data[index] = newLine

            with open(Website.uploads + '/login.txt', 'w', encoding='utf-8') as file:
                file.writelines(data)

        # CLIENT!
        def LoginAdd(self, ip : str, status : str, id : str):
            self.Unlogin(ip)
            logins = codecs.open(Website.uploads + '/login.txt', 'a', encoding="utf-8")
            logins.writelines(ip + ":" + status + ":" + id + ":" +"\n")
            logins.close()

        # CLIENT!
        def Login(self, username : str, password : str):
            if(not username or not password):
                return jsonify(message="Вы не ввели данные"), 400
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            print("\n" + "Клиент: " + client_ip)
            print(Fore.CYAN + "\nПопытка входа: " + username + " : " + password + Style.RESET_ALL)
            users_db = codecs.open(Website.uploads + '/users.txt', 'r', encoding="utf-8")
            for line in users_db:
                user = line.split(':')
                if(user[0] == username):
                    if(user[1] == password):
                        print(Fore.GREEN + "Успешный вход " + user[2] + ": " + username + Style.RESET_ALL + "\n")
                        users_db.close()
                        self.LoginAdd(client_ip, user[2], user[3])
                        return jsonify(message="Успешный вход, вы " + user[2]), 201
            print(Fore.RED + "Не успешный вход: " + username + Style.RESET_ALL + "\n")
            return jsonify(message="Данные не совпадают"), 400

    class Get:
        # CLIENT!
        def getUserById(self, user_id : str):
            if(not user_id):
                return jsonify(message="Вы не ввели индекс!"), 400
            user_db_read = codecs.open(Website.uploads + '/users.txt', 'r', encoding="utf-8")
            lines = user_db_read.readlines()
            user_db_read.close()
            for line in lines:
                cutLines = line.split(":")
                if(cutLines[3] == user_id):
                    if(cutLines[2] == "student"):
                        students_db_read = codecs.open(Website.uploads + '/students.txt', 'r', encoding="utf-8")
                        slines = students_db_read.readlines()
                        students_db_read.close()
                        for sline in slines:
                            cutLines = sline.split(":")
                            if(cutLines[0] == user_id):
                                student = Student(cutLines[2], cutLines[3], cutLines[4])
                                student.setId(user_id)
                                myDict = {'status': 'student', 'id': student.id, 'firstname': student.firstname, 'lastname': student.lastname, 'fathername': student.fathername, 'group': cutLines[0]}
                                return json.dumps(myDict, sort_keys=False), 200
                    if(cutLines[2] == "teacher"):
                        teachers_db_read = codecs.open(Website.uploads + '/teachers.txt', 'r', encoding="utf-8")
                        slines = teachers_db_read.readlines()
                        teachers_db_read.close()
                        for sline in slines:
                            scutLines = sline.split(":")
                            if(scutLines[0] == user_id):
                                teacher = Teacher(scutLines[1], scutLines[2], scutLines[3])
                                teacher.setId(user_id)
                                myDict = {'status': 'teacher', 'id': teacher.id, 'firstname': teacher.firstname, 'lastname': teacher.lastname, 'fathername': teacher.fathername, 'groups': []}
                                groups_db_read = codecs.open(Website.uploads + '/teachers_groups.txt', 'r', encoding="utf-8")
                                glines = groups_db_read.readlines()
                                groups_db_read.close()
                                for gline in glines:
                                    gcutLines = gline.split(":")
                                    if(gcutLines[0] == user_id):
                                        myDict["groups"].append(gcutLines[1])
                                return json.dumps(myDict, sort_keys=False), 200
                    if(cutLines[2] == "admin"):
                        myDict = {'status': 'admin', 'id': "admin", 'firstname': "admin", 'lastname': "admin", 'fathername': "admin"}
                        return json.dumps(myDict, sort_keys=False), 200
        #CLIENT!
        def getStudentsByGroup(self, group_index : str):
            if(not group_index ):
                return jsonify(message="Вы не ввели индекс группы"), 400

            myDict = {'Student': [{'id': 'None', 'firstname': 'None', 'lastname': 'None', 'fathername': 'None'}]}
            #
            #test = json.dumps(myDict,sort_keys=False)

            student_db_read = codecs.open(Website.uploads + '/students.txt', 'r', encoding="utf-8")
            lines = student_db_read.readlines()
            student_db_read.close()
            for line in lines:
                cutLines = line.split(":")
                if(cutLines[1] == group_index):
                    student = Student(cutLines[2], cutLines[3], cutLines[4])
                    student.setId(cutLines[0])
                    myDict['Student'].append(({'id': student.id, 'firstname': student.firstname, 'lastname': student.lastname, 'fathername': student.fathername}))
            del myDict["Student"][0]
            return json.dumps(myDict,sort_keys=False), 200

        #ДОДЕЛАТЬ! ПЕРЕДЕЛАТЬ С 2 АПРЕЛЯ
        #CLIENT!
        def getGroupByIndex(self, group_index : str):
            if(not group_index):
                return jsonify(message="Вы не ввели имя группы!"), 400
            group_db_read = codecs.open(Website.uploads + '/groups.txt', 'r', encoding="utf-8")
            lines = group_db_read.readlines()
            group_db_read.close()
            for line in lines:
                cutLines = line.split(":")
                if (cutLines[0] == group_index):
                    group = Group(cutLines[2], cutLines[3], cutLines[4])
                    myDict = {'id': cutLines[0], 'group': cutLines[2], 'course': cutLines[3], 'number': cutLines[4]}
                    return json.dumps(myDict,sort_keys=False), 200
            jsonify(message="Такой группы не существует!"), 400

        #CLIENT!
        def getCheckedAttendance(self, student_index : str):
            if(not student_index):
                return jsonify(message="Вы не ввели индекс ученика!"), 400

            attendances = {'Attendances': [{'id': 'None', 'student_id': 'None', 'Discipline': {'id': 'None', 'name': 'None'},'time': "None", 'reason': 'None', 'checked': 'None'}]}

            attendance_db_read = codecs.open(Website.uploads + '/attendance.txt', 'r', encoding="utf-8")
            lines = attendance_db_read.readlines()
            attendance_db_read.close()
            for line in lines:
                cutLines = line.split(":")
                if (cutLines[1] == student_index and cutLines[4] != "" and cutLines[4] != "Нет причины"):
                    checked = True
                    d_name = "None"
                    disciplines_db_read = codecs.open(Website.uploads + '/disciplines.txt', 'r', encoding="utf-8")
                    lines = disciplines_db_read.readlines()
                    disciplines_db_read.close()
                    for line in lines:
                        dcutLines = line.split(":")
                        if(dcutLines[0] == cutLines[2]):
                            d_name = dcutLines[1]
                            break
                    attendances['Attendances'].append(({'id': cutLines[0], 'student_id': cutLines[1], 'Discipline': {'id': cutLines[2], 'name': d_name}, 'time': cutLines[3], 'reason': cutLines[4], 'checked': checked}))
            del attendances['Attendances'][0]
            return json.dumps(attendances, sort_keys=False), 200

        #CLIENT!
        def getUnCheckedAttendance(self, student_index : str):
            if(not student_index):
                return jsonify(message="Вы не ввели индекс ученика!"), 400

            attendances = {'Attendances': [{'id': 'None', 'student_id': 'None', 'Discipline': {'id': 'None', 'name': 'None'},'time': "None", 'reason': 'None', 'checked': 'None'}]}

            attendance_db_read = codecs.open(Website.uploads + '/attendance.txt', 'r', encoding="utf-8")
            lines = attendance_db_read.readlines()
            attendance_db_read.close()
            for line in lines:
                cutLines = line.split(":")
                if (cutLines[1] == student_index and (cutLines[4] == "" or cutLines[4] == "Нет причины")):
                    checked = False
                    d_name = "None"
                    disciplines_db_read = codecs.open(Website.uploads + '/disciplines.txt', 'r', encoding="utf-8")
                    lines = disciplines_db_read.readlines()
                    disciplines_db_read.close()
                    for line in lines:
                        dcutLines = line.split(":")
                        if(dcutLines[0] == cutLines[2]):
                            d_name = dcutLines[1]
                            break
                    attendances['Attendances'].append(({'id': cutLines[0], 'student_id': cutLines[1], 'Discipline': {'id': cutLines[2], 'name': d_name}, 'time': cutLines[3], 'reason': cutLines[4], 'checked': checked}))
            del attendances['Attendances'][0]
            return json.dumps(attendances, sort_keys=False), 200

        #CLIENT!
        def getAllDisciplines(self):
            disciplines_db_read = codecs.open(Website.uploads + '/disciplines.txt', 'r', encoding="utf-8")
            lines = disciplines_db_read.readlines()
            disciplines_db_read.close()
            disciplines = {'Disciplines': [{'id': 'None', 'name': 'None'}]}
            for line in lines:
                cutLines = line.split(":")
                disciplines['Disciplines'].append(({'id': cutLines[0], 'name': cutLines[1]}))
            del disciplines["Disciplines"][0]
            return json.dumps(disciplines,sort_keys=False), 200

    class Post:
        #ADMIN
        def addAttendance(self, student_id : str, discipline_id : str, _datetime : str):
            if(not student_id or not discipline_id):
                return jsonify(message="Вы не введены корректные данные"), 400
            isStudent = False
            isDiscipline = False
            student_db_read = codecs.open(Website.uploads + '/students.txt', 'r', encoding="utf-8")
            lines = student_db_read.readlines()
            student_db_read.close()
            student_name = ""
            for line in lines:
                cutLines = line.split(":")
                if(cutLines[0] == student_id):
                    isStudent = True
                    student_name = cutLines[3]
            if(not isStudent):
                return jsonify(message="Такого ученика не существует"), 400
            discipline_db_read = codecs.open(Website.uploads + '/disciplines.txt', 'r', encoding="utf-8")
            lines = discipline_db_read.readlines()
            discipline_db_read.close()
            discipline_name = ""
            for line in lines:
                cutLines = line.split(":")
                if(cutLines[0] == discipline_id):
                    isDiscipline = True
                    discipline_name = cutLines[1]
            if(not isDiscipline):
                return jsonify(message="Такой дисциплины не существует"), 400
            attendance_db = codecs.open(Website.uploads + '/attendance.txt', 'a', encoding="utf-8")
            if(_datetime):
                lines = _datetime.split("-") # это если приходит в формате 10-04-2023-12-30 где (10-04-2023) - дата, (12-30) - время
                if(lines[0] and lines[1] and lines[2]and lines[3]and lines[4]):
                    _datetime = lines[0] + "-" + lines[1] + "-" + lines[2] + "-" + lines[3] + "-" + lines[4]
                else:
                    return jsonify(message="Время не того формата"), 400
            if(not _datetime):
                now = datetime.datetime.now()
                _datetime = now.strftime("%d-%m-%Y-%H-%M")
            attendance_db.writelines(Student.getRandomId() + ":" # это айди не студента а рандомное новое для посещаемости
                                     + student_id + ":"
                                     + discipline_id + ":"
                                     + _datetime + ":"
                                     + "Нет причины" + ":" + "\n")
            payload = {
                "app_id": Website.secrets["APP_ID"],
                "include_external_user_ids": [student_id],
                "channel_for_external_user_ids": "push",
                "isAndroid": True,
                "contents": {
                    "en": student_name + ", у вас новый прогул за " + _datetime + "\n" + discipline_name +" Укажите причину отсутствия!"
                },
                "name": "ВашаПосещаемость"
            }
            headers = {
                "accept": "application/json",
                "Authorization": "Basic " + Website.secrets["API_KEY"],
                "content-type": "application/json"
            }
            response = requests.post(Website.onesignal_url, json=payload, headers=headers)
            print("Отправка уведомления: " + response.text)
            return jsonify(message="Успешный учет отсутствия ученика " + student_id), 201

        #ADMIN
        def addUser(self, user, status : str):
            users_db_write = codecs.open(Website.uploads + '/users.txt', 'a', encoding="utf-8")
            users_db_write.writelines(translit((user.firstname + "_" + user.lastname + "_" + user.fathername), "ru", reversed=True)
                                                + ":" + ''.join(secrets.choice(alphabet) for i in range(10)
                                                + ":" + status + ":" + user.id)
                                                + ":" + "\n")
            users_db_write.close()

        #ADMIN
        def addStudent(self, student : Student, group_id : str):
            if(not student.firstname or not student.lastname or not student.fathername or not group_id):
                return jsonify(message="Вы не ввели какие-то данные"), 400
            isGroup = False
            group_db_read = codecs.open(Website.uploads + '/groups.txt', 'r', encoding="utf-8")
            lines = group_db_read.readlines()
            for line in lines:
                cutLines = line.split(":")
                if (cutLines[1].lower() == group_id or cutLines[0].lower() == group_id):
                    isGroup = True
                    break
            group_db_read.close()
            if(not isGroup):
                return jsonify(message="Не правильный индекс или название группы"), 400

            students_db_write = codecs.open(Website.uploads + '/students.txt', 'a', encoding="utf-8")
            students_db_write.writelines(str(student.id) + ":"
                                         + group_id + ":"
                                         + student.firstname + ":"
                                         + student.lastname + ":"
                                         + student.fathername + ":"
                                         + str(True) + ":" + "\n")
            students_db_write.close()
            self.addUser(student, "student")

            return jsonify(message="Ученик " + student.lastname + " был добавлен под индексом " + student.id), 201

        #ADMIN
        def addTeacher(self, teacher : Teacher):
            if(not teacher.firstname or not teacher.lastname or not teacher.fathername):
                return jsonify(message="Вы не ввели какие-то данные"), 400

            teachers_db_write = codecs.open(Website.uploads + '/teachers.txt', 'a', encoding="utf-8")
            teachers_db_write.writelines(str(teacher.id) + ":"
                                         + teacher.firstname + ":"
                                         + teacher.lastname + ":"
                                         + teacher.fathername + ":"
                                         + str(True) + ":" + "\n")
            teachers_db_write.close()

            self.addUser(teacher, "teacher")
            return jsonify(message="Учитель " + teacher.lastname + " был добавлен под индексом " + str(teacher.id)), 201

        #ADMIN
        def addGroup(self, group : Group):
            if(not group.number):
                return jsonify(message="Вы не указали номер!"), 400
            if(not group.speciality):
                return jsonify(message="Вы не указали специальность!"), 400
            if(not group.course):
                return jsonify(message="Вы не указали курс группы!"), 400

            group_db_write = codecs.open(Website.uploads + '/groups.txt', 'a', encoding="utf-8")
            group_db_write.writelines(str(group.id) + ":"
                                      + group.speciality + "-" + group.course + group.number + ":"
                                      + group.speciality + ":"
                                      + group.course
                                      + ":" + group.number
                                      + ":" + str(True) + ":" + "\n")
            group_db_write.close()
            return jsonify(message="Группа " + str(group) + " успешно добавлена под индексом " + group.id), 201

        #ADMIN
        def addGroupToTeacher(self, teacherId, groupId : str):
            tgroup_db_write = codecs.open(Website.uploads + '/teachers_groups.txt', 'a', encoding="utf-8")
            tgroup_db_write.writelines(teacherId + ":" + groupId + ":" + "\n")

        #ADMIN
        def addDiscipline(self, discipline : Discipline):
            if(discipline.name):
                return jsonify(message="Вы не ввели название дисциплины"), 400
            discipline_db_write = codecs.open(Website.uploads + '/disciplines.txt', 'a', encoding="utf-8")
            discipline_db_write.writelines(str(discipline.id) + ":"
                                           + discipline.name + ":" +"\n")
            discipline_db_write.close()
            return jsonify(message="Дисциплина " + str(discipline) + " успешно добавлена под индексом " + discipline.id), 201

    class Upload:

        #Client!
        def updateUserInfo(self):
            pass

        #Client!
        def updateAttendanceReason(self, attendance_id : str, reason : str):
            if(not attendance_id or not reason):
                return jsonify(message="Вы не ввели данные"), 201
            with codecs.open(Website.uploads + '/attendance.txt', 'r', encoding='utf-8') as file:
                data = file.readlines()

            time = ""
            for index, line in enumerate(data):
                data[index] = line.strip() + "\n"
                cutLines = line.split(":")
                if (cutLines[0] == attendance_id):
                    acutLines = line.split(":")
                    time = acutLines[3]
                    newLine = acutLines[0] + ":" + acutLines[1] + ":" + acutLines[2] + ":" + acutLines[3] + ":" + reason + ":" + "\n"
                    data[index] = newLine

            with open(Website.uploads + '/attendance.txt', 'w', encoding='utf-8') as file:
                file.writelines(data)

            if(time != ""):
                return jsonify(message="Отмечена причина отсутствия за " + time), 201
            else:
                return jsonify(message="Не существует отсутствия под таким индексом!"), 201

        #Client!
        def updateUserLogin(self, login : str, user_password : str):
            pass

        #Client!
        def updateUserPassword(self, login : str, user_password : str):
            pass