class Course:
    def __init__(self, name, instructor, room, time):
        self.name = name
        self.instructor = instructor
        self.room = room
        self.time = time

    def print(self):
        print(self.name + '  ' + self.instructor + '  ' + self.room + '  ' + str(self.time))