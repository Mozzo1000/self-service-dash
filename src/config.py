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

    def get_item(self, item, parent=None):
        if parent is None:
            parent = self.raw_config
        if item in parent:
            return parent[item]
        else:
            print(f"Key {item} does not exist in json file")
            return None