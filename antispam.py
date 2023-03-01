import time, math

from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
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
# - при запросе сохраняет инфу о ip клиента и о времени запроса в файл
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