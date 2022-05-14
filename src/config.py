import json
import sys
import os

class Config:
    def __init__(self, config_file="../examples/settings.json"):
        os.chdir(os.path.dirname(os.path.realpath(config_file)))
        try:
            with open(config_file, "r") as f:
                self.raw_config = json.load(f)
        except OSError:
            print(f"Failed to open {config_file}")
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
            print(f"Key {item} does not exist in json file.")
            return None