

class Project:
    def __init__(self, name, number, description):
        self.__name = name
        self.__number = number
        self.__description = description
    def getName(self):
        return self.__name
    def getNumber(self):
        return self.__number
    def getDescription(self):
        return self.__description
    def toTuple(self):
        return (self.getName(),self.getNumber(),self.getDescription())
    def toDict(self):
        return dict((\
                ('name',self.getName()),\
                ('number',self.getNumber()),\
                ('description',self.getDescription()),\
                ))


class DummyProjectDB:
    __projList = (\
            ('Project1', '1', 'The first project to choose'),\
            ('Project2', '2', 'The second project to choose'),\
            ('Project3', '3', 'Some other project'),\
            ('Project4', '4', 'Some other project'),\
            ('Project5', '5', 'Some other project'),\
            ('Project6', '6', 'Some other project'),\
            ('Project7', '7', 'Some other project'),\
            ('Project8', '8', 'Some other project'),\
            ('Project9', '9', 'Some other project'),\
            ('Project10', '10', 'Some other project'),\
            )
    def __init__(self, projectList=__projList):
        self.__projectList = dict((nu,Project(na,nu,de)) for na,nu,de in projectList)
        self.__students = {'5': ('Colin','8')}
    def getProjects(self):
        return iter(self.__projectList.values())
    def getProjectByNumber(self, number):
        return self.__projectList[number]
    def projectAvailable(self, number):
        return number not in self.__students
    def attributeProjectTo(self, number, student):
        self.__students[number] = student
    def getStudent(self, number):
        return self.__students[number]


