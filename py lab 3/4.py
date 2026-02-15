class StringHandler:
    def  getString(self):
        self.text = input()
    def printString(self):
        print(self.text.upper())
    
a=StringHandler()
a.getString()
a.printString()