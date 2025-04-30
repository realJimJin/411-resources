import logging
from app.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


class FavoriteLocation:
    """Represents a favorite location saved by a user.

    Stores attributes of the location ID, name of the location, latitude, longitude, description, and user. 
    Tracks the attributes of the location that is favorited and the User who saved it

    """
    def __init__(self, loc_id, name, lat, lng, description, user):
        """Initialize a new Favorite location instance with basic attributes.

        Args:
            loc_id (int): The location's ID. Must be unique.
            name (str): Name of location
            lat (float): Latitude of location
            lng (float): Longitide of location
            description (str): Short description of chosen location
            user (str):  user of the user who saved it

        """
        self.loc_id = loc_id
        self.name = name
        self.lat = lat
        self.lng = lng
        self.description = description
        self.user = user  # username of the owner

class FavoriteLocationModel:
    """In-memory model for storing favorite locations."""
    def __init__(self):
        self.locations = {}
        self.next_id = 1

    def add_location(self, name, lat, lng, description, user):
        """Add a new location to Users favorites

        Args:
            loc_id (int): The locations's ID. Must be unique.
            name (str): Name of location. 
            lat (float): Latitude of location
            lng (float): Longitide of location
            description (str): Short description of chosen location
            user (str):  user of the user who saved it

        Returns:
            loc (Favorite_Location): Created favorite location.

        """
        logger.info(f"Creating Location: {name}, {lat=} {lng=} {description=} {user=}")
        
        loc = FavoriteLocation(self.next_id, name, lat, lng, description, user)
        self.locations[self.next_id] = loc
        self.next_id += 1
        return loc


    def get_location(self, loc_id):
        """Retrieve a location by ID.

        Args:
            loc_id: The ID of the location.

        Returns:
            Favorite_Location: The Favorite location instance.

        Raises:
            ValueError: If the location with the given ID does not exist.

        """        
        logger.info(f"Looking for location with ID: {loc_id}")

        location = self.locations.get(loc_id)
        if location is None:
            logger.info(f"Location with ID {loc_id} not found.")
            raise ValueError(f"Location with ID {loc_id} not found.")
        return location

    def get_all_locations(self, user=None):
        """Retrieve all locations saved by a user.

        Args:
            user (str): Name of the user

        Returns:
            Favorite_Location: The Favorite location instance.

        Raises:
            ValueError: If given user does not exist.

        """ 
        logger.info(f"Attempting to get all locations {user}")

        if list(self.locations.values()) == None:
            logger.warning("No locations")
        if user:
            return [l for l in self.locations.values() if l.user == user]
        return list(self.locations.values())

    def update_location(self, loc_id, **kwargs):
        """Update the location

        Args:
            loc_id(int): ID of location that needs to be updated 

        Raises:
            ValueError: Location ID does not exist

        """
        location = self.locations.get(loc_id)
        if location is None:
            logger.info(f"Location with ID {loc_id} not found.")
            raise ValueError(f"Location with ID {loc_id} not found.")

        for k, v in kwargs.items():
            if hasattr(location, k):
                setattr(location, k, v)
        return location

    def delete_location(self, loc_id):
        """Delete a location by ID.

        Args:
            loc_id: The ID of the location to delete.

        Raises:
            ValueError: If the location with the given ID does not exist.

        """

        location = self.locations.get(loc_id)
        if location is None:
            logger.info(f"Location with ID {loc_id} not found.")
            raise ValueError(f"Location with ID {loc_id} not found.")
        return self.locations.pop(loc_id, None)

favorite_locations_model = FavoriteLocationModel()