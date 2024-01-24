import arcgis
from arcgis.gis import GIS
from optional import optional

def connect(org_url: str, login_name: str, user_password: str, profile_name: optional=None):
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
            log_profile_info(gis)
            return gis
        except Exception as e:
            login_failed_message = f"Unable to connect to {org_url} with the profile '{profile_name}'. Please check your credentials and try again."
            print(login_failed_message)
            return False
    else:
        print(f'No profile specified, attempting connection {org_url} using username: {login_name} and password')
        try:
            gis = GIS(url=org_url, username=login_name, password=user_password)
            try: 
                log_profile_info(gis)
            except Exception as e:
                print('error: log_profile_info method is missing')
            return gis
        except Exception as e:
            login_failed_message = f'Unable to connect to {org_url}. Please check your credentials and try again.'
            print(login_failed_message)
            return False

def log_profile_info(gis):
    '''
    Output print statement that displays gis properties
    '''
    print("Successfully logged into '{}' via the user '{}'".format(
        gis.properties.portalHostname,
        gis.properties.user.username))


def get_gis_item(item_id: str, gis: GIS):
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
        print(f"Successfully retrived GIS Item ID: {item_id}")
        return item
