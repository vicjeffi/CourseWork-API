import uuid, json

class Group:
    def __init__(self, speciality : str, course : str, number : str):
        self.id = uuid.uuid4().hex
        self.course = course
        self.number = number
        self.speciality = speciality
        
    def setId(self, id : str):
        self.id = id

    def setStudents(self, count : int):
        self.students_count = count

    def __str__(self):
        return f'{self.speciality}-{self.course}{self.number}'
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)