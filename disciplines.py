import uuid, json

class Discipline:
    def __init__(self, name):
        self.id = uuid.uuid4().hex
        self.name = name

    def __str__(self):
        return f'{self.name}'
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)