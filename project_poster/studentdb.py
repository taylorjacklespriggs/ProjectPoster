

class CSVStudentDB:
    def __init__(self, filename):
        self.students = set()
        with open(filename, 'r') as csv:
            for name, number in (line.split(',')\
                    for line in csv.read().split('\n') if len(line)):
                self.students.add((name, number))
    def studentExists(self, name, number):
        return (name, number) in self.students


class DummyStudentDB:
    def __init__(self, studentList):
        self.studentList = studentList
    def studentExists(self, name, number):
        return (name, number) in self.studentList


