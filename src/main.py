from PyQt5.QtWidgets import QApplication, QMenu, QSystemTrayIcon
from PyQt5.QtGui import QIcon, QCursor, QPainter, QPixmap, QImage
import sys
from config import Config
from menuitem import MenuItem


class App:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.config = Config()
        self.notification_state = False

        if self.config.get_mode() == "tray":
            self.icon = QImage(self.config.get_item("icon"))

            self.menu = QMenu()
            self.menu.setToolTipsVisible(True)

            for item in self.config.get_item("menu"):
                menu_it = MenuItem(app=self, parent=self.menu,
                                   title=self.config.get_item(
                                       "title", parent=item),
                                   icon=self.config.get_item(
                                       "icon", parent=item),
                                   type=self.config.get_item(
                                       "type", parent=item),
                                   action=self.config.get_item(
                                       "action", parent=item),
                                   options=self.config.get_item("options", parent=item))
                self.menu.addAction(menu_it.get_action())

            

            self.tray = QSystemTrayIcon()
            self.tray.activated.connect(self.showMenuOnTrigger)
            self.tray.setToolTip(self.config.get_item("title"))
            self.tray.setIcon(QIcon(QPixmap.fromImage(self.icon)))
            self.tray.setContextMenu(self.menu)
            self.tray.show()

    def showMenuOnTrigger(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.menu.popup(QCursor.pos())

    def run(self):
        # Enter Qt application main loop
        self.app.exec_()
        sys.exit()


if __name__ == "__main__":
    app = App()
    app.run()
