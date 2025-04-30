import pytest
from app.models.favorite_location import FavoriteLocationModel
def fav_model():
    """Fixture providing a fresh FavoriteLocationModel for each test."""
    return FavoriteLocationModel()

@pytest.fixture
def sample_location_data():
    """Fixture providing sample location input data."""
    return {
        "name": "Eiffel Tower",
        "lat": 48.8584,
        "lng": 2.2945,
        "description": "Iconic Paris landmark",
        "user": "testuser"
    }


# Add Location

def test_add_location(fav_model, sample_location_data):
    """Test adding a new favorite location."""
    loc = fav_model.add_location(**sample_location_data)
    assert loc.name == sample_location_data["name"]
    assert loc.lat == sample_location_data["lat"]
    assert loc.lng == sample_location_data["lng"]
    assert loc.description == sample_location_data["description"]
    assert loc.user == sample_location_data["user"]
    assert loc.loc_id == 1  

# Get Location

def test_get_location_existing(fav_model, sample_location_data):
    """Test retrieving an existing favorite location."""
    loc = fav_model.add_location(**sample_location_data)
    fetched = fav_model.get_location(loc.loc_id)
    assert fetched == loc

def test_get_location_nonexistent(fav_model):
    """Test retrieving a non-existent favorite location."""
    with pytest.raises(ValueError, match="not found"):
        fav_model.get_location(999)


# Get All Locations

def test_get_all_locations(fav_model, sample_location_data):
    """Test getting all locations."""
    fav_model.add_location(**sample_location_data)
    fav_model.add_location(name="Louvre Museum", lat=48.8606, lng=2.3376, description="Famous museum", user="testuser")
    all_locations = fav_model.get_all_locations()
    assert len(all_locations) == 2

def test_get_all_locations_for_user(fav_model, sample_location_data):
    """Test getting locations filtered by user."""
    fav_model.add_location(**sample_location_data)
    fav_model.add_location(name="Louvre Museum", lat=48.8606, lng=2.3376, description="Famous museum", user="anotheruser")
    user_locations = fav_model.get_all_locations(user="testuser")
    assert len(user_locations) == 1
    assert user_locations[0].user == "testuser"



# Update Location

def test_update_location_existing(fav_model, sample_location_data):
    """Test updating an existing favorite location."""
    loc = fav_model.add_location(**sample_location_data)
    updated = fav_model.update_location(loc.loc_id, name="Updated Tower", description="Updated description")
    assert updated.name == "Updated Tower"
    assert updated.description == "Updated description"

def test_update_location_nonexistent(fav_model):
    """Test updating a non-existent location."""
    with pytest.raises(ValueError, match="not found"):
        fav_model.update_location(9999)

# Delete Location

def test_delete_location_existing(fav_model, sample_location_data):
    """Test deleting an existing favorite location."""
    loc = fav_model.add_location(**sample_location_data)
    deleted = fav_model.delete_location(loc.loc_id)
    assert deleted is not None
    assert fav_model.get_location(loc.loc_id) is None

def test_delete_location_nonexistent(fav_model):
    """Test deleting a non-existent favorite location."""
    deleted = fav_model.delete_location(999)
    assert deleted is None