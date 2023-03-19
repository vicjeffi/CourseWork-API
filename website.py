from antispam import antiSpam
from students import Student
from groups import Group

from flask import request, jsonify
import codecs

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

import secrets
import string

from transliterate import translit

alphabet = string.ascii_letters + string.digits
class Website:
    name = ""
    def __init__(self, name):
        self.name = name
        self.post = self.Post()
        self.get = self.Get()
        self.admin = self.Admin()

    class Admin:
        def getClientId(self):
            if(not self.getIsClientLogined()):
                return "None"
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            logins = codecs.open('uploads/login.txt', 'r', encoding="utf-8")
            for line in logins:
                lines = line.split(':')
                if(lines[0] == client_ip):
                    logins.close()
                    return lines[2]
            logins.close()
        
        def getClientStatus(self):
            if(not self.getIsClientLogined()):
                return "None"
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            logins = codecs.open('uploads/login.txt', 'r', encoding="utf-8")
            for line in logins:
                lines = line.split(':')
                if(lines[0] == client_ip):
                    logins.close()
                    return lines[1]
            logins.close()
        
        def getIsClientLogined(self):
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            logins = codecs.open('uploads/login.txt', 'r', encoding="utf-8")
            for line in logins:
                lines = line.split(':')
                if(lines[0] == client_ip):
                    logins.close()
                    return True
            logins.close()
            return False
        
        def showInfo(self):
            return jsonify(
                logined = self.getIsClientLogined(),
                status = self.getClientStatus(),
                ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr),
                id = self.getClientId()
            )
        
        def Unlogin(self, ip = ""):
            if(ip == ""):
                ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            with open("uploads/login.txt", "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i.__contains__(ip):
                        print(Fore.LIGHTCYAN_EX + "Пользователь вышел из профиля: " + i + Style.RESET_ALL)
                        f.write("")
                f.truncate()

        # Удаляет все прошлые логины пользователя и добавляет новый
        def LoginAdd(self, ip, status, id):
            self.Unlogin(ip)
            logins = codecs.open('uploads/login.txt', 'a', encoding="utf-8")
            logins.writelines(ip + ":" + status + ":" + id + ":" +"\n")
            logins.close()
        
        # adminLogin() func
        # - проверяет доступ админа к управнию системы
        # - выводит сообщения о попытке клиента, доступе
        def Login(self, username, password):
            if(not username or not password):
                print(self.Login.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не ввели данные"), 200
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            print("\n" + "Клиент: " + client_ip)
            print(Fore.CYAN + "\nПопытка входа: " + username + " : " + password + Style.RESET_ALL)
            users_db = open('uploads/users.txt', 'r')
            for line in users_db:
                user = line.split(':')
                if(user[0] == username):
                    if(user[1] == password):
                        print(Fore.GREEN + "Успешный вход " + user[2] + ": " + username + Style.RESET_ALL + "\n")
                        users_db.close()
                        self.LoginAdd(client_ip, user[2], user[3])
                        return jsonify(message="Успешный вход, вы " + user[2]), 201
            print(Fore.RED + "Внимание! Не успешный вход: " + username + Style.RESET_ALL + "\n")
            return jsonify(message="Данные не совданают"), 201

    class Get:
        def getStudentById(self, student_id):
            if(not student_id):
                print(self.getStudentById.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не ввели индекс ученика"), 200
            student_db_read = codecs.open('uploads/students.txt', 'r', encoding="utf-8")
            lines = student_db_read.readlines()
            student_db_read.close()
            for line in lines:
                cutLines = line.split(":")
                if(cutLines[0] == student_id):
                    print(self.getStudentById.__name__ + " удачно!" + "\n")
                    student = Student(cutLines[2], cutLines[3], cutLines[4])
                    student.setId(student_id)
                    return student.toJSON()

        def getStudentByGroupAndId(self, group_id, student_index):
            if(not group_id or not student_index):
                print(self.getStudentByGroupAndId.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не ввели индекс ученика или группы"), 200
            if(int(student_index) < 0):
                print(self.getStudentByGroupAndId.__name__ + " неудачно!" + "\n")
                return jsonify(message="Индекс должен быть больше нуля"), 200
            groupIndex = ""
            group_db_read = codecs.open('uploads/groups.txt', 'r', encoding="utf-8")
            lines = group_db_read.readlines()
            group_db_read.close()
            for line in lines:
                cutLines = line.split(":")
                if (cutLines[1].lower() == group_id.lower() or cutLines[0].lower() == group_id.lower()):
                    groupIndex = cutLines[0]
                    break
            if(groupIndex == ""):
                print(self.getGroupIndexByName.__name__ + " неудачно!" + "\n")
                return jsonify(message="Не правильный индекс или название группы"), 200
            # ДОДЕЛАТЬ
            cashIndex = 0
            student_db_read = codecs.open('uploads/students.txt', 'r', encoding="utf-8")
            lines = student_db_read.readlines()
            student_db_read.close()
            for line in lines:
                cutLines = line.split(":")
                if(cutLines[1] == groupIndex):
                    if(int(student_index) == cashIndex):
                        print(self.getStudentById.__name__ + " удачно!" + "\n")
                        student = Student(cutLines[2], cutLines[3], cutLines[4])
                        student.setId(cutLines[0])
                        student.setGroup(cutLines[1])
                        return student.toJSON(), 201
                    cashIndex += 1
            return jsonify(message="Ученика под таких номером нету"), 200
        
        #GET индекса группы по названию
        def getGroupByName(self, group_name):
            if(not group_name):
                print(self.getGroupByName.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не ввели имя группы!"), 200
            group_db_read = codecs.open('uploads/groups.txt', 'r', encoding="utf-8")
            lines = group_db_read.readlines()
            group_db_read.close()
            for line in lines:
                cutLines = line.split(":")
                if (cutLines[1].lower() == group_name.lower()):
                    group = Group(cutLines[2], cutLines[3], cutLines[4])
                    group.setId(cutLines[0])
                    student_db_read = codecs.open('uploads/students.txt', 'r', encoding="utf-8")
                    lines = student_db_read.readlines()
                    student_db_read.close()
                    for line in lines:
                        cutLines = line.split(":")
                        if(cutLines[1] == group.id):
                            group.setStudents(group.students_count + 1)
                    return group.toJSON(), 201
            return jsonify(message="Группы c таким именем не существует!"), 200
        
    class Post:
        def addAttendance(self, student_id, discipline_name):
            if(Website.Admin.checkLogin(True) != "teacher"):
                print(self.addAttendance.__name__ + " неудачно!" + "\n")
                return jsonify(message="Учитель, войдите в аккаунт!"), 200
            if(not student_id or not discipline_name):
                print(self.addAttendance.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не введи данные"), 200
            attendance_db = codecs.open('uploads/groups.txt', 'a', encoding="utf-8")
            attendance_db.writelines(Student.getRandomId + ":" 
                                     + student_id + ":" 
                                     + discipline_name + ":" 
                                     + "Нет причины" + ":" + "\n")
            print(self.addAttendance.__name__ + " успешно!" + "\n")
            jsonify(message="Успешное добавление прогула ученика под id " + student_id), 201

        def addStudent(self, student, group_id):
            if(not student.firstname or not student.lastname or not student.fathername or not group_id):
                print(self.addStudent.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не ввели какие-то данные"), 200
            isGroup = False
            group_db_read = codecs.open('uploads/groups.txt', 'r', encoding="utf-8")
            lines = group_db_read.readlines()
            for line in lines:
                cutLines = line.split(":")
                if (cutLines[1].lower() == group_id or cutLines[0].lower() == group_id):
                    isGroup = True
                    break
            if(not isGroup):
                print(self.addStudent.__name__ + " неудачно!" + "\n")
                return jsonify(message="Не правильный индекс или название группы"), 200

            students_db_write = codecs.open('uploads/students.txt', 'a', encoding="utf-8")
            students_db_write.writelines(str(student.id) + ":" 
                                         + group_id + ":" 
                                         + student.firstname + ":" 
                                         + student.lastname + ":" 
                                         + student.fathername + ":" 
                                         + str(True) + ":" + "\n")
            students_db_write.close()
            users_db_write = codecs.open('uploads/users.txt', 'a', encoding="utf-8")
            users_db_write.writelines(translit((student.firstname + "_" + student.lastname + "_" + student.fathername 
                                                + ":" + ''.join(secrets.choice(alphabet) for i in range(10)
                                                + ":" + "student" + ":" + student.id)
                                                + ":" + "\n"), "ru", reversed=True))
            print(self.addStudent.__name__ + " удачно!" + "\n")
            return jsonify(message="Ученик " + student.lastname + " был добавлен под индексом " + str(student.id)), 201
        
        def addGroup(self, group):
            if(not group.number):
                print(self.addGroup.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не указали номер!"), 200
            if(not group.speciality):
                print(self.addGroup.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не указали специальность!"), 200
            if(not group.course):
                print(self.addGroup.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не указали курс группы!"), 200
            
            group_db_write = codecs.open('uploads/groups.txt', 'a', encoding="utf-8")
            group_db_write.writelines(str(group.id) + ":" 
                                      + group.speciality + "-" + group.course + group.number + ":" 
                                      + group.speciality + ":" 
                                      + group.course 
                                      + ":" + group.number 
                                      + ":" + str(True) + ":" + "\n")
            group_db_write.close()
            print(self.addGroup.__name__ + " удачно!" + "\n")
            return jsonify(message="Группа " + str(group) + " успешно добавлена под индексом "), 201
            
        
        def addDiscipline(self, discipline):
            if(discipline.name):
                print(self.addDiscipline.__name__ + " неудачно!" + "\n")
                return jsonify(message="Вы не ввели название дисциплины"), 200
            discipline_db_write = codecs.open('uploads/disciplines.txt', 'a', encoding="utf-8")
            discipline_db_write.writelines(str(discipline.id) + ":" 
                                           + discipline.name + ":" +"\n")
            discipline_db_write.close()
            print(self.addDiscipline.__name__ + " удачно!" + "\n")
            return jsonify(message="Дисциплина " + str(discipline) + " успешно добавлена под индексом " + discipline.id), 201
            
            