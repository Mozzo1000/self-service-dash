from PyQt5.QtWidgets import QAction, QApplication
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import QUrl

class MenuItem:
    def __init__(self, parent, title=None, icon=None, type=None, action=None):
        self.parent = parent
        self.title = title
        self.icon = icon
        self.type = type
        self.action = action
        self.action_item = None

        if type != "separator":
            self.action_item = QAction(QIcon(self.icon), self.title, self.parent)
            print(self.action)
            self.action_item.triggered.connect(lambda: self.parse_action())
        elif type == "separator":
            parent.addSeparator()

    def get_action(self):
        return self.action_item

    def parse_action(self):
        if self.type == "builtin":
            if self.action == "quit":
                return QApplication.instance().quit()
        elif self.type == "link":
            return QDesktopServices.openUrl(QUrl(self.action))