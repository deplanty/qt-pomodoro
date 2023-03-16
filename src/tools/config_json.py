import json


class ConfigJson(dict):
    def __init__(self, filename:str):
        self.filename = filename

        with open(filename, encoding="utf-8") as fid:
            self.update(json.load(fid))

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as fid:
            json.dump(self, fid)
