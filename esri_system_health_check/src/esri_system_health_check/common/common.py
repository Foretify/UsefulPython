import os
import sys
import logging
from arcgis.gis import GIS, Item
from typing import Optional, Text
from datetime import datetime, timedelta
from configparser import ConfigParser, RawConfigParser


def connect(org_url: str, login_name: str, user_password: str, profile_name: Optional[str]=None):
    """Authenticate and connect to an ArcGIS organization. The GIS is used to access, manage
    and modify a users content.

    Args:
        org_url (str): This should be a web address to either an ArcGIS Enterprise portal or to ArcGIS Online in the 
                        form: <scheme>://<fully_qualified_domain_name>/<web_adaptor> (ArcGIS Enterprise example)
        login_name (str): The login user name (case-sensitive).
        user_password (str): If a username is provided, a password is expected. This is case-sensitive.
        profile_name (str, optional): The name of the profile that the user wishes to use to authenticate, if set, 
                                        the identified profile will be used to login to the specified GIS. Defaults to None.
    """
    if profile_name:
        print(f'Attempting to connect with the credential profile, {profile_name}')
        try:
            gis = GIS(profile=profile_name)
            print_profile_info() 
            return gis
        except Exception as e:
            login_failed_message = f"Unable to connect to {org_url} with the profile '{profile_name}'. Please check your credentials and try again."
            print(login_failed_message)
            print(e, exc_info=True)
            return None
    else:
        print('No profile specified menaing no profile was stored on the system.\nAttempting to connect using username and password for ArcGIS:\n')
        try:
            gis = GIS(url=org_url, username=login_name, password=user_password)
            print_profile_info(gis)
            return gis
        except Exception as e:
            login_failed_message = f'Unable to connect to {org_url}. Please check your credentials and try again.'
            print(login_failed_message)
            print(e, exc_info=True)
            return None


def get_gis_item(item_id: str, gis: GIS) -> Item:
        """ This is a method that retrieves a layer from AGOL or Enterprise by retrieving the layer based
            on the item id and the GIS config object

        Args:
            item_id (str): Item ID of the content that is requested and returned as an item object 
            gis (arcgis.gis.GIS): GIS authentication object that's passed in to access item.  Note, user must
            have access to item in order to fulfill the request.    

        Raises:
            Exception: Message that is returned in regards to unable to access item.

        Returns:
            arcgis.gis.Item: Item content object for the requested item id.
        """
        print(f"Attempting to retrieve layer with item id: {item_id}")
        item = gis.content.get(item_id)

        if not item:
            item_not_found_message = f"Input Item ID Not Found in GIS: {item_id}"
            print(item_not_found_message)
            raise Exception(item_not_found_message)
        else:
            print(f"Successfully got GIS Item ID: {item_id}")
            return item


def print_profile_info(gis):
        '''
        Output print statement that displays gis properties
        '''
        print("Successfully logged into '{}' via the user '{}'".format(
            gis.properties.portalHostname,
            gis.properties.user.username))



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
        print(f"Configuration for {config_type} is not a valid. Valid configuration files are {', '.join(list(configs.keys()))}")
        sys.exit()

    config_path = os.path.join(
        configs[config_type]['path'], configs[config_type]['file'])

    # Check if configuration file exists.
    if os.path.exists(config_path):
        return config_path
    else:
        print(f"Configuration file at {config_path} does not exist.")
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


def process_edits(feature_layer, data_frame, operation, batch_count=10):
    """
    Push edits from SDF to hosted feature layer.
    """

    print(f"Running {operation.upper()} on Hosted Feature Layer")

    # Chunk edits into lists of 500 items. Python API can only push so many updates; item sized based on bytes.
    update_sets = list(batch_it(data_frame.spatial.to_featureset().features, batch_count))

    for edits in update_sets:
        if operation == 'update':
            res = feature_layer.edit_features(updates=edits, rollback_on_failure=False)['updateResults']
            logger.info(f"Updated {len([i for i in res if i['success']])} rows of {len(edits)}")
        else:
            res = feature_layer.edit_features(adds=edits, rollback_on_failure=False)['addResults']
            logger.info(f"Added {len([i for i in res if i['success']])} rows of {len(edits)}")


def time_bound_clause(datetime_field: str, time_range: int) -> Text:
    """Create a where statement to look back at a specified time range in minutes. Time is converted to UTC
    Args:
        datetime_field (str): Field name from layer that is of the data type datetime.
        time_range (int): Value in the unit of minutes.
    Returns:
        Text: A string formatted as a complete SQL clause. 
    """
    look_back_time = (datetime.utcnow() - timedelta(hours=0, minutes=time_range)).strftime('%Y-%m-%d %H:%M:%S')
    where_clause = f"{datetime_field} >= timestamp'{look_back_time}'"
    return where_clause


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

def batch_it(l, n):

    for i in range(0, len(l), n):
        yield l[i:i + n]
        
        
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
        
    