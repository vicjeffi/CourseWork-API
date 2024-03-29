import uuid, json
class Student:
    def __init__(self, firstname : str, lastname : str, fathername : str):
        self.id = uuid.uuid4().hex
        self.firstname = firstname
        self.lastname = lastname
        self.fathername = fathername
        self.group = ""

    def setGroup(self, groupId : str):
        if(groupId):
            self.group = groupId
    
    def setId(self, Id : str):
        if(Id):
            self.id = Id

    def __str__(self):
        return f'id:{self.id} ' \
               f'Firstname: {self.firstname}; ' \
               f'Lastname: {self.lastname}; ' \
               f'Fathername: {self.fathername}' \
               f'Group: {self.group}; '
    
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
    def getRandomId():
        return uuid.uuid4().hex