class dataRead():
    def __init__(self,body,mumba):
        self.body = body;
        self.mumba = mumba;
        print(self.mumba)
def data(x2):
    dataRead.body = 10;
    dataRead.mumba = x2;
    #print(dataRead.mumba)
data(40)