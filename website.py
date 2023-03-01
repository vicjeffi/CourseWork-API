from antispam import antiSpam

from flask import request
import codecs

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

class Website:
    name = ""
    def __init__(self, name):
        self.name = name
    
# adminLogin() func
# подключена antiSpam система!
# - проверяет доступ админа к управнию системы
# - выводит сообщения о попытке клиента, доступе и резутата проверки антиспам системы

def adminUnloginAll():
    admin_logins = codecs.open('uploads/admins_login.txt', 'w', encoding="utf-8")
    admin_logins.close()

def adminLoginAdd(ip):
    admin_logins = codecs.open('uploads/admins_login.txt', 'a', encoding="utf-8")
    admin_logins.writelines(ip + "\n")
    admin_logins.close()
def adminCheck():
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
    print("\n" + "Клиент: " + client_ip)
    admin_db = open('uploads/admins_login.txt', 'r')
    for line in admin_db:
        print(line)
        if(line.__contains__(client_ip)):
            print(Fore.GREEN + "Успешный вход админа под ip: " + client_ip + Style.RESET_ALL)
            return True
    return False

def adminLogin(username, password, text):
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
                    adminLoginAdd(client_ip)
                    return True
                print(Fore.RED + "Не правильный пороль!" + Style.RESET_ALL)
    antiSpam.Add(client_ip)
    print(Fore.RED + "Внимание! Не успешный вход админа: " + username + Style.RESET_ALL + "\n")
    return False

def addStudent(student_name, student_lastname, student_fathername):
    if(student_name and student_lastname and student_fathername):
        students_db_read = open('uploads/students.txt', 'r')
        sudents_count = 0
        for s_line in students_db_read:
            sudents_count += 1

        students_db_write = codecs.open('uploads/students.txt', 'a', encoding="utf-8")
        students_db_write.writelines(str(sudents_count) + ":" + student_lastname + ":" + student_name + ":" + student_fathername + ":" + str(True) + "\n")

        students_db_write.close()
        students_db_read.close()

        print(addStudent.__name__ + " удачно!" + "\n")
        return "Ученик " + student_name + " был добавлен под индексом " + str(sudents_count), 200

    print(addStudent.__name__ + " не удачно!" + "\n")
    return "Err: Вы не указали имя, фамилию или отчество студента!", 400