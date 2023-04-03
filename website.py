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

from transliterate import translit

alphabet = string.ascii_letters + string.digits
class Website:
    name = ""
    uploads = "uploads" # на хосте "mysite/uploads"
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
            with open(Website.uploads + "/login.txt", "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i.__contains__(ip):
                        print(Fore.LIGHTCYAN_EX + "Пользователь вышел из профиля: " + i + Style.RESET_ALL)
                        f.write("")
                f.truncate()

        # CLIENT!
        def LoginAdd(self, ip : str, status : str, id : str):
            self.Unlogin(ip)
            logins = codecs.open(Website.uploads + '/login.txt', 'a', encoding="utf-8")
            logins.writelines(ip + ":" + status + ":" + id + ":" +"\n")
            logins.close()

        # CLIENT!
        def Login(self, username : str, password : str):
            if(not username or not password):
                print(self.Login.__name__ + " неудачно!" + "\n")
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
            print(Fore.RED + "Внимание! Не успешный вход: " + username + Style.RESET_ALL + "\n")
            return jsonify(message="Данные не совпадают"), 400

    class Get:
        # CLIENT!
        def getUserById(self, user_id : str):
            if(not user_id):
                print(self.getStudentById.__name__ + " неудачно!" + "\n")
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
                print(self.getStudentByGroupAndId.__name__ + " неудачно!" + "\n")
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
        def getGroupByName(self, group_name : str):
            if(not group_name):
                print(self.getGroupByName.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не ввели имя группы!"), 400
            group_db_read = codecs.open(Website.uploads + '/groups.txt', 'r', encoding="utf-8")
            lines = group_db_read.readlines()
            group_db_read.close()
            for line in lines:
                cutLines = line.split(":")
                if (cutLines[1].lower() == group_name.lower()):
                    group = Group(cutLines[2], cutLines[3], cutLines[4])
                    group.setId(cutLines[0])
                    student_db_read = codecs.open(Website.uploads + '/students.txt', 'r', encoding="utf-8")
                    lines = student_db_read.readlines()
                    student_db_read.close()
                    for line in lines:
                        cutLines = line.split(":")
                        if(cutLines[1] == group.id):
                            group.setStudents(group.students_count + 1)
                    return group.toJSON(), 201
            return jsonify(message="Группы c таким именем не существует!"), 400

        #CLIENT!
        def getAllAttendance(self, student_index : str):
            pass

        #CLIENT!
        def getUnCheckedAttendance(self, student_index : str):
            pass
        
    class Post:

        #ADMIN
        def addAttendance(self, student_id : str, discipline_name : str, _datetime : str):
            if(not student_id or not discipline_name or discipline_name.__contains__(":")):
                print(self.addAttendance.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не введены корректные данные"), 400
            attendance_db = codecs.open(Website.uploads + '/attendance.txt', 'a', encoding="utf-8")
            if(_datetime):
                lines = _datetime.split("-") # это если приходит в формате 10-04-2023-12-30 где (10-04-2023) - дата, (12-30) - время
                _datetime = lines[0] + "-" + lines[1] + "-" + lines[2] + "-" + lines[3] + " " + lines[4] + ":"
            if(not _datetime):
                now = datetime.now()
                _datetime = now.strftime("%d-%m-%Y-%H-%M")
            attendance_db.writelines(Student.getRandomId() + ":" # это айди не студента а рандомное новое для посещаемости
                                     + _datetime + ":"
                                     + student_id + ":"
                                     + discipline_name + ":"
                                     + "Нет причины" + ":" + "\n")
            print(self.addAttendance.__name__ + " успешно!" + "\n")
            jsonify(message="Успешное добавление прогула ученика под id " + student_id), 201

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
                print(self.addStudent.__name__ + " неудачно!" + "\n")
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
                print(self.addStudent.__name__ + " неудачно!" + "\n")
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

            print(self.addStudent.__name__ + " удачно!" + "\n")
            return jsonify(message="Ученик " + student.lastname + " был добавлен под индексом " + student.id), 201
        
        #ADMIN
        def addTeacher(self, teacher : Teacher):
            if(not teacher.firstname or not teacher.lastname or not teacher.fathername):
                print(self.addTeacher.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не ввели какие-то данные"), 400

            teachers_db_write = codecs.open(Website.uploads + '/teachers.txt', 'a', encoding="utf-8")
            teachers_db_write.writelines(str(teacher.id) + ":"
                                         + teacher.firstname + ":"
                                         + teacher.lastname + ":"
                                         + teacher.fathername + ":"
                                         + str(True) + ":" + "\n")
            teachers_db_write.close()
            
            self.addUser(teacher, "teacher")
            
            print(self.addTeacher.__name__ + " удачно!" + "\n")
            return jsonify(message="Учитель " + teacher.lastname + " был добавлен под индексом " + str(teacher.id)), 201
        
        #ADMIN
        def addGroup(self, group : Group):
            if(not group.number):
                print(self.addGroup.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не указали номер!"), 400
            if(not group.speciality):
                print(self.addGroup.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не указали специальность!"), 400
            if(not group.course):
                print(self.addGroup.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не указали курс группы!"), 400

            group_db_write = codecs.open(Website.uploads + '/groups.txt', 'a', encoding="utf-8")
            group_db_write.writelines(str(group.id) + ":"
                                      + group.speciality + "-" + group.course + group.number + ":"
                                      + group.speciality + ":"
                                      + group.course
                                      + ":" + group.number
                                      + ":" + str(True) + ":" + "\n")
            group_db_write.close()
            print(self.addGroup.__name__ + " удачно!" + "\n")
            return jsonify(message="Группа " + str(group) + " успешно добавлена под индексом " + group.id), 201

        #ADMIN
        def addGroupToTeacher(self, teacherId, groupId : str):
            tgroup_db_write = codecs.open(Website.uploads + '/teachers_groups.txt', 'a', encoding="utf-8")
            tgroup_db_write.writelines(teacherId + ":" + groupId + ":" + "\n")

        #ADMIN
        def addDiscipline(self, discipline : Discipline):
            if(discipline.name):
                print(self.addDiscipline.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не ввели название дисциплины"), 400
            discipline_db_write = codecs.open(Website.uploads + '/disciplines.txt', 'a', encoding="utf-8")
            discipline_db_write.writelines(str(discipline.id) + ":"
                                           + discipline.name + ":" +"\n")
            discipline_db_write.close()
            print(self.addDiscipline.__name__ + " удачно!" + "\n")
            return jsonify(message="Дисциплина " + str(discipline) + " успешно добавлена под индексом " + discipline.id), 201
        
    class Upload:

        #Client!
        def updateUserInfo(self):
            pass

        #Client!
        def updateAttendanceReason(self, reason : str):
            pass

        #Client!
        def updateUserLogin(self, login : str, user_password : str):
            pass

        #Client!
        def updateUserPassword(self, login : str, user_password : str):
            pass