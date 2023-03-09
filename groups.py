import uuid, json

class Group:
    students_count = 0
    def __init__(self, speciality, course, number):
        self.id = uuid.uuid4().hex
        self.course = course
        self.number = number
        self.speciality = speciality
        

    def setId(self, id):
        self.id = id

    def setStudents(self, count):
        self.students_count = count

    def __str__(self):
        return f'{self.speciality}-{self.course}{self.number}'
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)