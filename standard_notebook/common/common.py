import sys
import os
import logging
logger = logging.getLogger(__name__)

from configparser import ConfigParser, RawConfigParser

from typing import Optional, Text


def test():
    print("This works well")

def get_config_path(config_type: Optional[str]="main configuration") -> str:
    """

    Args:
        config_type (Optional[str], optional): specify the type of configuration 
        file. Defaults to "main configuration". configuration types that can be return are:
            - "main configuration"
            - "logging configuration"

    Returns:
        str: File path to the selected configuration file.
    """

    this_dir = os.path.dirname(__file__)
    root_dir = os.path.abspath(os.path.join(this_dir, os.pardir))

    # Default configuration paths
    configs = {
        'main configuration': {'path': os.path.join(root_dir, 'config'), 'file': 'config.ini'},
        'logging configuration': {'path': os.path.join(root_dir, 'config'), 'file': 'log_config.ini'}
    }

    if config_type not in list(configs.keys()):
        logger.error(f"Configuration for {config_type} is not a valid. Valid configuration files are {', '.join(list(configs.keys()))}")
        sys.exit()

    config_path = os.path.join(
        configs[config_type]['path'], configs[config_type]['file'])

    # Check if configuration file exists.
    if os.path.exists(config_path):
        return config_path
    else:
        logger.error(f"Configuration file at {config_path} does not exist.")
        sys.exit()


def load_configuration(config_path: str, raw: Optional [bool]=False) -> ConfigParser:
    """ Read in the configuration file and convert to a ConfigParser object

    Args:
        config_path (str): Filepath to configuration file.
        raw (bool, optional): Property that that can return with the RawconfigPaser object.

    Returns:
        ConfigParser: return a ConfigParser object
    """
    if raw:
        config = RawConfigParser()
    else:
        config = ConfigParser()
    config.read(config_path)

    return config

def write_config_param(payload: dict, config_file: Optional[str]="logging configuration"):
    """ Method to save changes back to a configuration file.

    Args:
        payload (dict): Payload dictionary that contains a dictionary of dictionaries. The outer
        dictionary represents the section name of the configuration file. The inner dictionary contains
        the one or more parameter names and the corresponding value. 

        config_file (Optional[str], optional): Specify the configuration file that the payload
        will be saved to. Defaults to "logging configuration" to update the log_config.ini file.
    """

    config_file_path = get_config_path(config_type=config_file)
    parser = load_configuration(config_file_path, raw=True)

    # Loop through each of the section and set the new values
    for group, param in payload.items():
        if group not in parser.sections():
            parser.add_section(group)
        for key, value in param.items():
            parser.set(group, key, value)

    # Save changes to config file
    with open(config_file_path, 'w+') as configfile:
        parser.write(EqualsSpaceRemover(configfile))


class EqualsSpaceRemover:
    '''
    The write function from the configparser library adds a space in the front/end of the = sign.
    The extra space causes issues with the batch file reading in the config parameters from the .ini file.
    This class replaces " = " with "=" in all lines of the config file.
    
    See this stackexchange question for more info: https://stackoverflow.com/questions/14021135/how-to-remove-spaces-while-writing-in-ini-file-python/25084055#25084055
    '''
    output_file = None

    def __init__(self, new_output_file):
        self.output_file = new_output_file

    def write(self, what):
        self.output_file.write(what.replace(" = ", "=", 1))

        