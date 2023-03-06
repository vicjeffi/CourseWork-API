import uuid, json

class Group:
    def __init__(self, speciality, course, number):
        self.id = uuid.uuid4().hex
        self.number = number
        self.speciality = speciality
        self.course = course

    def __str__(self):
        return f'{self.speciality}-{self.course}{self.number}'
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)