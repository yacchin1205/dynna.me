import os
import json
from uuid import uuid4

def load_config(config_path):
    if not os.path.exists(config_path):
        save_config(config_path, generate_config())
    with open(os.path.expanduser(config_path), 'r') as f:
        return json.load(f)

def save_config(config_path, config):
    with open(os.path.expanduser(config_path), 'w') as f:
        json.dump(config, f)

def generate_config():
    r = {}
    r['secret'] = str(uuid4())
    return r
