class Record:
    broker = ""
    client = ""
    data = []

    def __init__(self, broker, client):
        self.broker = broker
        self.client = client
    
    def setData(self, med_list):
        self.data = med_list
    
    def addData(self, medData):
        self.data.append(medData)

    def printData(self):
        for i in range(len(self.data)):
            print(self.data[i])