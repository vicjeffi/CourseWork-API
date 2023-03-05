import uuid

class Group:
    def __init__(self, speciality, course, number):
        self.id = uuid.uuid4().hex
        self.number = number
        self.speciality = speciality
        self.course = course

    def __str__(self):
        return f'{self.speciality}-{self.course}{self.number}'