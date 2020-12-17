import json


class ConfigManager:
    config = {}

    @classmethod
    def initialize_config(cls, input_config=None):
        if not input_config:
            with open("configFile.json", "r") as json_file:
                cls.config = json.load(json_file)
        else:
            cls.config = input_config

    @classmethod
    def fetch(cls, key):
        return cls.config[key]
