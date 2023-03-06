from antispam import antiSpam
from students import Student
from groups import Group

from flask import request, jsonify
import codecs

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

class Website:
    name = ""
    def __init__(self, name):
        self.name = name
        self.post = self.Post()
        self.get = self.Get()
        self.admin = self.Admin()
    
    class Admin:
        # adminLogin() func
        # подключена antiSpam система!
        # - проверяет доступ админа к управнию системы
        # - выводит сообщения о попытке клиента, доступе и резутата проверки антиспам системы
        def adminUnloginAll(self):
            admin_logins = codecs.open('uploads/admins_login.txt', 'w', encoding="utf-8")
            admin_logins.close()

        def adminLoginAdd(self, ip):
            admin_logins = codecs.open('uploads/admins_login.txt', 'a', encoding="utf-8")
            admin_logins.writelines(ip + "\n")
            admin_logins.close()

        def adminCheck(self):
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            print("\n" + "Клиент: " + client_ip)
            admin_db = open('uploads/admins_login.txt', 'r')
            for line in admin_db:
                if(line.__contains__(client_ip)):
                    print(Fore.GREEN + "Успешный вход админа под ip: " + client_ip + Style.RESET_ALL)
                    return True
            return False

        def adminLogin(self, website, username, password, text):
            client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
            print("\n" + "Клиент: " + client_ip)
            print(Fore.CYAN + "\nПопытка входа админа: " + username + ":" + password + " с целью: '" + text + "'" + Style.RESET_ALL)
            if(username != "" and username and password != "" and password):
                admin_db = open('uploads/admins.txt', 'r')

                #Добавить юзабельность хэшеру!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                #hasher = PSWHash256()
                
                for line in admin_db:
                    user = line.split(':')
                    if(user[0] == username): #хэшер здесь!
                        if(user[1] == password): #и здесь!
                            print(Fore.GREEN + "Успешный вход админа: " + username + Style.RESET_ALL)
                            admin_db.close()
                            website.ad.adminLoginAdd(client_ip)
                            return True
                        print(Fore.RED + "Не правильный пороль!" + Style.RESET_ALL)
            antiSpam.Add(client_ip)
            print(Fore.RED + "Внимание! Не успешный вход админа: " + username + Style.RESET_ALL + "\n")
            return False
    
    # ПРОВЕРИТЬ КАК РАБОТАЕТ ГЕТЫ ДОМА
    class Get:
        def getStudentById(self, student_id):
            if(student_id):
                student_db_read = codecs.open('uploads/students.txt', 'r', encoding="utf-8")
                for line in student_db_read.readlines():
                    cutLines = line.split(":")
                    if(cutLines[0] == student_id):
                        print(self.getStudentById.__name__ + " удачно!" + "\n")
                        student = Student(cutLines[2], cutLines[3], cutLines[4])
                        student.setId(student_id)
                        return student.toJSON()
            return "Вы не ввели индекс ученика", 401

        def getStudentByGroupAndIndex(self, group_id, student_index):
            if(group_id and student_index):
                if(student_index < 0 ):
                    return "Индекс должен быть больше нуля", 401
                groupIndex = ""
                group_db_read = codecs.open('uploads/groups.txt', 'r', encoding="utf-8")
                lines = group_db_read.readlines()
                for line in lines:
                    cutLines = line.split(":")
                    if (cutLines[1].lower() == group_id or cutLines[0].lower() == group_id):
                        groupIndex = cutLines[0]
                        break
                if(groupIndex == ""):
                    print(self.addStudent.__name__ + " неудачно!" + "\n")
                    return "Не правильный индекс или название группы", 402
                # ДОДЕЛАТЬ
                cashIndex = 0
                student_db_read = codecs.open('uploads/students.txt', 'r', encoding="utf-8")
                for line in student_db_read.readlines():
                    cutLines = line.split(":")
                    if(cutLines[0] == groupIndex):
                        if(student_index == cashIndex):
                            print(self.getStudentById.__name__ + " удачно!" + "\n")
                            student = Student(cutLines[2], cutLines[3], cutLines[4])
                            student.setId(cutLines[0])
                            student.setGroup(cutLines[1])
                            return student.toJSON()
                    cashIndex += 1
                return "Ученика под таких номером нету", 403
            return "Вы не ввели индекс ученика или группы", 401
        
        #GET индекса группы по названию
        
    class Post:
        def addStudent(self, student, group_id):
            if(student.firstname and student.lastname and student.fathername and group_id):
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
                    return "Не правильный индекс или название группы", 402

                students_db_write = codecs.open('uploads/students.txt', 'a', encoding="utf-8")
                students_db_write.writelines(str(student.id) + ":" + group_id + ":" + student.firstname + ":" + student.lastname + ":" + student.fathername + ":" + str(True) + "\n")
                students_db_write.close()

                print(self.addStudent.__name__ + " удачно!" + "\n")
                return "Ученик " + student.lastname + " был добавлен под индексом " + str(student.id), 201

            print(self.addStudent.__name__ + " не удачно!" + "\n")
            return "Err: Вы не указали имя, фамилию или отчество студента!", 400
        
        def addGroup(self, group):
            if(group.number and group.speciality and group.course):
                group_db_write = codecs.open('uploads/groups.txt', 'a', encoding="utf-8")
                group_db_write.writelines(str(group.id) + ":" + group.speciality + "-" + group.course + group.number + ":" + group.speciality + ":" + group.course + ":" + group.number + ":" + str(True) + "\n")
                print(self.addGroup.__name__ + " удачно!" + "\n")
                return "Группа " + str(group) + " успешно добавлена под индексом " + group.id, 213
            print(self.addGroup.__name__ + " неудачно!" + "\n")
            return "Вы не указали номер группы", 402