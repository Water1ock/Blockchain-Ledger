class User:
    name = ""
    password = ""

    def __init__(self, n, p):
        self.name = n
        self.password = p

    def setPass(self, pw):
        self.password = pw

    def setName(self, nm):
        self.name = nm

    def getName(self):
        return self.name

    def getPass(self):
        return self.password

    def validate(a, b):
        if(a == b):
            return True
        return False