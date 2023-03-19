import uuid, json
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
    
    def setId(self, Id):
        if(Id):
            self.id = Id

    def __str__(self):
        return f'id:{self.id} ' \
               f'Firstname: {self.firstname}; ' \
               f'Lastname: {self.lastname}; ' \
               f'Fathername: {self.fathername}' \
               f'Group: {self.group}; '
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)
    
    def getRandomId():
        return uuid.uuid4().hex