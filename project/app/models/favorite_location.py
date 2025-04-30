import logging
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from project.utils.logger import configure_logger


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
            name (str): Name of location. Must be unique
            lat (float): Latitude of location
            lng (float): Longitide of location
            description (str): Short description of chosen location
            user (str):  user of the user who saved it

        Returns:
            loc (Favorite_Location): New favorite location

        Raises:
            IntegrityError: If a boxer with the same name already exists.
            SQLAlchemyError: If there is a database error during creation.

        """
        logger.info(f"Creating Location: {name}, {lat=} {lng=} {description=} {user=}")
        try:
            loc = FavoriteLocation(self.next_id, name, lat, lng, description, user)
            self.locations[self.next_id] = loc
            self.next_id += 1
            logger.info(f"Location created successfully")
            return loc
        except IntegrityError:
            db.session.rollback()
            logger.error(f"Location with name '{name}' already exists.")
            raise ValueError(f"Location with name '{name}' already exists.")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during creation: {e}")
            raise


    def get_location(cls, loc_id):
        """Retrieve a location by ID.

        Args:
            loc_id: The ID of the location.

        Returns:
            Favorite_Location: The Favorite location instance.

        Raises:
            ValueError: If the location with the given ID does not exist.

        """        
        location = cls.locations.get(loc_id)
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
        if user is None:
            logger.info(f"User with name {user} not found.")
            raise ValueError(f"User with name {user} not found.")
        if user:
            return [l for l in self.locations.values() if l.user == user]
        return list(self.locations.values())

    def update_location(cls, loc_id, **kwargs):
        """Update the location

        Args:
            loc_id(int): ID of location that needs to be updated 

        Raises:
            ValueError: Location ID does not exist

        """
        location = cls.locations.get(loc_id)
        if location is None:
            logger.info(f"Location with ID {loc_id} not found.")
            raise ValueError(f"Location with ID {loc_id} not found.")

        for k, v in kwargs.items():
            if hasattr(location, k):
                setattr(location, k, v)
        return location

    def delete_location(cls, loc_id):
        """Delete a location by ID.

        Args:
            loc_id: The ID of the location to delete.

        Raises:
            ValueError: If the location with the given ID does not exist.

        """
        try:
            location = cls.locations.pop(loc_id, None)
            db.session.delete(location)
            db.session.commit()
            logger.info(f"Location with ID {loc_id} deleted successfully.")
        except ValueError as e:
            logger.error(f"Error deleting location: {e}")
            raise
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during deletion: {e}")
            raise

favorite_locations_model = FavoriteLocationModel()