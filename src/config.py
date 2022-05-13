import json
import sys

class Config:
    def __init__(self):
        try:
            with open("settings.json", "r") as f:
                self.raw_config = json.load(f)
        except OSError:
            print("Failed to open settings.json")
            sys.exit()
    
    def get_mode(self):
        if "mode" in self.raw_config:
            if self.raw_config["mode"] == "tray":
                return "tray"
            elif self.raw_config["mode"] == "window":
                return "window"
            else:
                print("Unknown mode, defaulting to tray")
                return "tray"
        else:
            print("No mode set, defaulting to tray")
            return "tray"

    def get_item(self, item, parent=None):
        if parent is None:
            parent = self.raw_config
        if item in parent:
            return parent[item]
        else:
            print(f"Key {item} does not exist in json file")
            return None