import os
import configparser
from pathlib import Path
from typing import Dict, Union
from .confi
gs import Config


def get_config_properties(file_name: str) -> Dict[str, Dict[str, str]]:
    """Return the variables found in a user specified .ini file in the configurations folder.

    Args:
        file_name (str): Name of the configuration file found in the configurations folder. Note, file type suffix is
        not required to pass in.  By default we only accept .ini files.

    Returns:
        Dict[str, Any]: Dictionary of the sections and items in the configuration file.
    """
    # Create configparser object and read in the configuration file.
    config = configparser.ConfigParser()
    config.read(os.path.join(CONFIG_DIR, f"{file_name}.ini"))

    # Convert config parser object into a dictionary. First level dictionary key is the section name
    # and the second level dictionary are the section key names.
    return config.__dict__["_sections"]


def get_project_root() -> Union[str, os.PathLike]:
    """Grab the root directory of this project.

    NOTE, this variable is relatively referenced. If this file is moved, path's that depend on this
    method will generate the correct path.

    Returns:
        Union[str, os.PathLike]:: Root path of this project represented as a string
    """
    return str(Path(__file__).parent.parent.parent)


# Grab folder paths to referenced directories and files.
ROOT_DIR = get_project_root()
CONFIG_DIR = os.path.join(ROOT_DIR, "configurations")
NOTEBOOK_PATH = os.path.join(ROOT_DIR, "resources", "notebooks")
DATA_DIR = os.path.join(ROOT_DIR, "data")
SPACY_ASSETS = os.path.join(DATA_DIR, "assets")
OUTPUT_DIR = os.path.join(DATA_DIR, "output")
MODEL_DIR = os.path.join(DATA_DIR, "models")

# Create class objects that contain our configuration file details
DATABASE_SETTINGS = Config(os.path.join(CONFIG_DIR, "main_config.ini"), "Database Settings")
