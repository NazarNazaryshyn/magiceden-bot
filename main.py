import json
import magiceden
import os

def get_config():
    config_file = open('config.json', 'r')
    return list(json.load(config_file).values())

config = get_config()

is_windows = True if os.name == 'nt' else False


magiceden.mint(config, is_windows)