from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import QUrl
import sys
import json
from config import Config
from menuitem import MenuItem

class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.config = Config()

        if self.config.get_mode() == "tray":
            #print(self.config.raw_config)
            #print(self.config.raw_config["menu"][0])

            icon = QIcon(self.config.get_item("icon"))
            menu = QMenu()

            for item in self.config.get_item("menu"):
                menu_it = MenuItem(parent=menu,
                                    title=self.config.get_item("title", parent=item),
                                    icon=self.config.get_item("icon", parent=item),
                                    type=self.config.get_item("type", parent=item),
                                    action=self.config.get_item("action", parent=item))
                menu.addAction(menu_it.get_action())

            self.tray = QSystemTrayIcon()
            self.tray.setToolTip(self.config.get_item("title"))
            self.tray.setIcon(icon)
            self.tray.setContextMenu(menu)
            self.tray.show()

    def run(self):
        # Enter Qt application main loop
        self.app.exec_()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.run()