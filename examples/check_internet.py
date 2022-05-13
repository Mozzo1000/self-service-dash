from urllib.request import urlopen

class CheckInternet:
    def __init__(self, parent):
        self.parent = parent
        self.parent.action_item.setEnabled(False)
        self.checkConnection()
    
    def onLoop(self):
        self.checkConnection()

    def checkConnection(self):
        try:
            urlopen("https://google.com", timeout=10)
            self.parent.change_title("Connected to internet!")   
        except:
            self.parent.change_title("Not connected to internet")