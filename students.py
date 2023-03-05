import uuid
class Student:
    group = ""
    def __init__(self, firstname, lastname, fathername):
        self.id = uuid.uuid4().hex
        self.firstname = firstname
        self.lastname = lastname
        self.fathername = fathername

    def setGroup(self, groupId):
        if(groupId):
            self.group = groupId

    def __str__(self):
        return f'id:{self.id} ' \
               f'Firstname: {self.firstname}; ' \
               f'Lastname: {self.lastname}; ' \
               f'Fathername: {self.fathername}' \
               f'Group: {self.group}; '