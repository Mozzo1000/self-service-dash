from PyQt5.QtWidgets import QAction, QApplication
from PyQt5.QtGui import QIcon, QDesktopServices
from PyQt5.QtCore import QUrl
import importlib.util
import inspect
import os
from threading import Thread, Timer
import time

class MenuItem:
    def __init__(self, parent, title=None, icon=None, type=None, action=None, options=None):
        self.parent = parent
        self.title = title
        self.icon = icon
        self.type = type
        self.action = action
        self.options = options
        self.action_item = None
        print(options)

        if type != "separator":
            self.action_item = QAction(QIcon(self.icon), self.title, self.parent)
            print(self.action)
            self.parse_action()
        elif type == "separator":
            parent.addSeparator()

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
                self.action_item.triggered.connect(lambda: QApplication.instance().quit())
        elif self.type == "link":
            self.action_item.triggered.connect(lambda: QDesktopServices.openUrl(QUrl(self.action)))
        elif self.type == "script":
            return self.call_script()

    def call_script(self):
        try: 
            spec = importlib.util.spec_from_file_location(self.action, os.path.join(os.getcwd(), self.action + ".py"))
            plugin = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(plugin)
            for name_local in dir(plugin):
                if inspect.isclass(getattr(plugin, name_local)):
                    Class = getattr(plugin, name_local)
                    plugin_object = Class(self)
                    if self.options:
                        if "repeat" in self.options:
                            thread = Thread(target=self.background_task, args=(plugin_object,self.options["repeat"]), daemon=True)
                            thread.start()
                    
                    self.action_item.triggered.connect(lambda: plugin_object.onClick())
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