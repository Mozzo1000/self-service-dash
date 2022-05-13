from distutils.log import set_verbosity
import platform

class GetVersion:
    def __init__(self, parent):
        self.parent = parent
        self.setVersion()

    def onClick(self):
        self.setVersion()

    def setVersion(self):
        if platform.system() == "Windows":
            self.parent.change_title("Version: Windows " + platform.release())
        elif platform.system() == "Darwin":
            self.parent.change_title("Version: macOS " + platform.release())
        elif platform.system() == "Linux":
            self.parent.change_title("Version: Linux " + platform.release())
        else:
            self.parent.change_title("Version: Can't find version number")