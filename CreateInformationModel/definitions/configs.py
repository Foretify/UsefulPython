import configparser
from dataclasses import dataclass
import ast
from typing import Dict, Union


@dataclass
class Config:
    def __init__(self, config_file_path: str, section: str):
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(config_file_path)
        config_dict: Dict[str, Union[str, int, float, bool, None]] = self.config_parser[section]

        for key, value in config_dict.items():
            try:
                value = ast.literal_eval(value)
            except (ValueError, SyntaxError):
                pass
            setattr(self, key, value)
