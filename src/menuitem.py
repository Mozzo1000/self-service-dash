from PyQt5.QtWidgets import QAction, QApplication
from PyQt5.QtGui import QIcon, QDesktopServices, QImage, QPainter, QPixmap
from PyQt5.QtCore import QUrl
import importlib.util
import inspect
import os
from threading import Thread
import time
import subprocess


class MenuItem:
    def __init__(self, app, parent, title=None, icon=None, type=None, action=None, options=None):
        self.app = app
        self.parent = parent
        self.title = title
        self.icon = icon
        self.type = type
        self.action = action
        self.options = options
        self.action_item = None

        if type == "separator":
            parent.addSeparator()
        elif type == "submenu":
            sub_menu = self.parent.addMenu(self.title)
            for item in self.app.config.get_item("menu"):
                menu_list = self.app.config.get_item("menu_list", parent=item)
                if menu_list:
                    for i in menu_list:
                        sub_menu.addAction(MenuItem(app=self.app, parent=self.parent,
                                            title=self.app.config.get_item(
                                                "title", parent=i),
                                            icon=self.app.config.get_item(
                                                "icon", parent=i),
                                            type=self.app.config.get_item(
                                                "type", parent=i),
                                            action=self.app.config.get_item(
                                                "action", parent=i),
                                            options=self.app.config.get_item("options", parent=i)).get_action())
                        

        else:
            self.action_item = QAction(
                QIcon(self.icon), self.title, self.parent)
            self.parse_action()

    def get_action(self):
        return self.action_item

    def change_title(self, name):
        self.title = name
        self.action_item.setText(name)

    def set_tooltip(self, name):
        self.action_item.setToolTip(name)

    def parse_action(self):
        if self.type == "builtin":
            if self.action == "quit":
                self.action_item.triggered.connect(
                    lambda: QApplication.instance().quit())
        elif self.type == "link":
            self.action_item.triggered.connect(
                lambda: QDesktopServices.openUrl(QUrl(self.action)))
        elif self.type == "script":
            return self.call_script()
        elif self.type == "application":
            return self.run_app()
        elif self.type.startswith("text"):
            self.action_item.setEnabled(False)
            if self.type == "text:enabled":
                self.action_item.setEnabled(True)            

    def run_app(self):
        self.action_item.triggered.connect(
            lambda: subprocess.Popen(self.action))

    def call_script(self):
        try:
            spec = importlib.util.spec_from_file_location(
                self.action, os.path.join(os.getcwd(), self.action + ".py"))
            plugin = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin)
            for name_local in dir(plugin):
                if inspect.isclass(getattr(plugin, name_local)):
                    Class = getattr(plugin, name_local)
                    plugin_object = Class(self)
                    if self.options:
                        if "repeat" in self.options:
                            thread = Thread(target=self.background_task, args=(
                                plugin_object, self.options["repeat"]), daemon=True)
                            thread.start()

                    self.action_item.triggered.connect(
                        lambda: plugin_object.onClick())
        except ModuleNotFoundError:
            print("Script not found")
            self.change_title("Could not load script: " + self.action)
            self.action_item.setEnabled(False)

    def background_task(self, plugin, interval):
        while True:
            try:
                plugin.onLoop()
                time.sleep(interval)
            except AttributeError:
                print("No onLoop found in plugin: " + str(plugin))
                break
    
    def set_notification_pending(self, state=True):
        self.app.notification_state = state
        if state:
            overlay = QImage(self.app.config.get_item("notification_overlay"))
            painter = QPainter()
            painter.begin(self.app.icon)
            painter.drawImage(0, int(self.app.icon.height() - overlay.height()), overlay)
            painter.end()
            self.app.tray.setIcon(QIcon(QPixmap.fromImage(self.app.icon)))
        else:
            self.app.icon = QImage(self.app.config.get_item("icon"))
            self.app.tray.setIcon(QIcon(QPixmap.fromImage(self.app.icon)))
    
    def get_notification_state(self):
        return self.app.notification_state