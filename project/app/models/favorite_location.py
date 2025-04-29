class FavoriteLocation:
    """Represents a favorite location saved by a user."""
    def __init__(self, loc_id, name, lat, lng, description, user):
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
        loc = FavoriteLocation(self.next_id, name, lat, lng, description, user)
        self.locations[self.next_id] = loc
        self.next_id += 1
        return loc

    def get_location(self, loc_id):
        return self.locations.get(loc_id)

    def get_all_locations(self, user=None):
        if user:
            return [l for l in self.locations.values() if l.user == user]
        return list(self.locations.values())

    def update_location(self, loc_id, **kwargs):
        loc = self.get_location(loc_id)
        if not loc:
            return None
        for k, v in kwargs.items():
            if hasattr(loc, k):
                setattr(loc, k, v)
        return loc

    def delete_location(self, loc_id):
        return self.locations.pop(loc_id, None)

favorite_locations_model = FavoriteLocationModel()