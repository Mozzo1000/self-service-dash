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
            self.parent.set_tooltip("Build: " + platform.version())
        elif platform.system() == "Darwin":
            self.parent.change_title("Version: macOS " + platform.release())
            self.parent.set_tooltip("Build: " + platform.version())
        elif platform.system() == "Linux":
            self.parent.change_title("Version: Linux " + platform.release())
            self.parent.set_tooltip("Build: " + platform.version())
        else:
            self.parent.change_title("Version: Can't find version number")
            self.parent.set_tooltip("Build: Can't find build number")