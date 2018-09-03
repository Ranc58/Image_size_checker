import os
from typing import Dict
import yaml

CONFIG_PATH = os.path.join(os.getcwd(), 'config', 'conf.yaml')


def get_config() -> Dict:
    with open(CONFIG_PATH) as f:
        config = yaml.load(f)
    return config


config = get_config()
