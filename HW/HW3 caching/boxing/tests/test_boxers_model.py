import pytest

from boxing.models.boxers_model import Boxers

# --- Fixtures ---

@pytest.fixture
def boxer_ali(session):
    """Fixture for Muhammad Ali."""
    boxer = Boxers(name="Muhammad Ali", weight=210, height=191, reach=78, age=32)
    session.add(boxer)
    session.commit()
    return boxer

@pytest.fixture
def boxer_tyson(session):
    """Fixture for Mike Tyson."""
    boxer = Boxers(name="Mike Tyson", weight=220, height=178, reach=71, age=35)
    session.add(boxer)
    session.commit()
    return boxer


# --- Create Boxer ---

<<<<<<< HEAD
def test_clear_ring(ring_model):
     """Test that clear_ring empties the ring."""
     ring_model.ring = [1, 2]
     ring_model.clear_ring()
     assert len(ring_model.ring) == 0
#def test_clear_ring(): return True

def test_clear_ring_empty(ring_model, caplog):
     """Test that clear_ring logs a warning when already empty."""
     with caplog.at_level("WARNING"):
         ring_model.clear_ring()
     assert len(ring_model.ring) == 0
     assert "Attempted to clear an empty ring." in caplog.text
#def test_clear_ring_empty(): return True

def test_get_boxers_empty(ring_model, caplog):
     """Test get_boxers logs when empty."""
     with caplog.at_level("WARNING"):
         boxers = ring_model.get_boxers()
     assert boxers == []
     assert "Retrieving boxers from an empty ring." in caplog.text
# def test_get_boxers_empty(): return True

def test_get_boxers_with_data(app, ring_model, sample_boxers):
     """Test get_boxers with two sample boxers."""
     ring_model.ring.extend([b.id for b in sample_boxers])
     boxers = ring_model.get_boxers()
     assert boxers == sample_boxers
#def test_get_boxers_with_data(): return True

def test_get_boxers_uses_cache(ring_model, sample_boxer1, mocker):
     ring_model.ring.append(sample_boxer1.id)
     ring_model._boxer_cache[sample_boxer1.id] = sample_boxer1
     ring_model._ttl[sample_boxer1.id] = time.time() + 100
     mock_get = mocker.patch("boxing.models.ring_model.Boxers.get_boxer_by_id")
     boxers = ring_model.get_boxers()
     assert boxers[0] == sample_boxer1
     mock_get.assert_not_called()
#def test_get_boxers_uses_cache(): return True

def test_get_boxers_refreshes_on_expired_ttl(ring_model, sample_boxer1, mocker):
     ring_model.ring.append(sample_boxer1.id)
     ring_model._boxer_cache[sample_boxer1.id] = mocker.Mock()
     ring_model._ttl[sample_boxer1.id] = time.time() - 1
     mock_get = mocker.patch("boxing.models.ring_model.Boxers.get_boxer_by_id", return_value=sample_boxer1)
     boxers = ring_model.get_boxers()
     assert boxers[0] == sample_boxer1
     mock_get.assert_called_once_with(sample_boxer1.id)
#def test_get_boxers_refreshes_on_expired_ttl(): return True

def test_cache_populated_on_get_boxers(ring_model, sample_boxer1, mocker):
     mock_get = mocker.patch("boxing.models.ring_model.Boxers.get_boxer_by_id", return_value=sample_boxer1)
     ring_model.ring.append(sample_boxer1.id)
     boxers = ring_model.get_boxers()
     assert sample_boxer1.id in ring_model._boxer_cache
     assert sample_boxer1.id in ring_model._ttl
     assert boxers[0] == sample_boxer1
#def test_cache_populated_on_get_boxers(): return True

def test_enter_ring(ring_model, sample_boxers, app):
     ring_model.enter_ring(sample_boxers[0].id)
     assert ring_model.ring == [sample_boxers[0].id]
     ring_model.enter_ring(sample_boxers[1].id)
     assert ring_model.ring == [sample_boxers[0].id, sample_boxers[1].id]
#def test_enter_ring(): return True

def test_enter_ring_full(ring_model):
     ring_model.ring = [1, 2]
     with pytest.raises(ValueError, match="Ring is full"):
         ring_model.enter_ring(3)
#def test_enter_ring_full(): return True
=======
def test_create_boxer(session):
    """Test creating a new boxer."""
    Boxers.create_boxer("Joe Frazier", 205, 180, 75, 33)
    boxer = session.query(Boxers).filter_by(name="Joe Frazier").first()
    assert boxer is not None
    assert boxer.weight_class == "HEAVYWEIGHT"
>>>>>>> upstream/solutions


def test_create_boxer_duplicate_name(session, boxer_ali):
    """Test creating a boxer with a duplicate name."""
    with pytest.raises(ValueError, match="already exists"):
        Boxers.create_boxer("Muhammad Ali", 200, 180, 72, 30)

<<<<<<< HEAD
def test_get_fighting_skill(ring_model, sample_boxers):
     expected_1 = 210 * 12 + (78 / 10)
     expected_2 = 220 * 10 + (71 / 10) - 1
     assert ring_model.get_fighting_skill(sample_boxers[0]) == expected_1
     assert ring_model.get_fighting_skill(sample_boxers[1]) == expected_2
#def test_get_fighting_skill(): return True

def test_fight(ring_model, sample_boxers, caplog, mocker):
     ring_model.ring.extend(sample_boxers)
     mocker.patch("boxing.models.ring_model.RingModel.get_fighting_skill", side_effect=[2526.8, 2206.1])
     mocker.patch("boxing.models.ring_model.get_random", return_value=0.42)
     mocker.patch("boxing.models.ring_model.RingModel.get_boxers", return_value=sample_boxers)
     mock_update = mocker.patch("boxing.models.ring_model.Boxers.update_stats")
     winner = ring_model.fight()
     assert winner == "Muhammad Ali"
     mock_update.assert_any_call("win")
     mock_update.assert_any_call("loss")
     assert ring_model.ring == []
#def test_fight(): return True

def test_fight_with_empty_ring(ring_model):
     with pytest.raises(ValueError, match="There must be two boxers to start a fight."):
         ring_model.fight()
#def test_fight_with_empty_ring(): return True

def test_fight_with_one_boxer(ring_model, sample_boxer1):
     ring_model.ring.append(sample_boxer1)
     with pytest.raises(ValueError, match="There must be two boxers to start a fight."):
         ring_model.fight()
#def test_fight_with_one_boxer(): return True

def test_clear_cache(ring_model, sample_boxer1):
     ring_model._boxer_cache[sample_boxer1.id] = sample_boxer1
     ring_model._ttl[sample_boxer1.id] = time.time() + 100
     ring_model.clear_cache()
     assert ring_model._boxer_cache == {}
     assert ring_model._ttl == {}
#def test_clear_cache(): return True
=======

@pytest.mark.parametrize("name, weight, height, reach, age, err_msg", [
    ("TooLight", 100, 170, 70, 25, "Weight must be at least 125."),
    ("NoHeight", 140, 0, 70, 25, "Height must be greater than 0."),
    ("NoReach", 140, 170, 0, 25, "Reach must be greater than 0."),
    ("TooYoung", 140, 170, 70, 17, "Age must be between 18 and 40."),
    ("TooOld", 140, 170, 70, 45, "Age must be between 18 and 40."),
])
def test_create_boxer_invalid_data(name, weight, height, reach, age, err_msg):
    """Test validation errors when creating a boxer."""
    with pytest.raises(ValueError, match=err_msg):
        Boxers.create_boxer(name, weight, height, reach, age)


# --- Get Boxer ---

def test_get_boxer_by_id(boxer_ali):
    """Test fetching a boxer by ID."""
    fetched = Boxers.get_boxer_by_id(boxer_ali.id)
    assert fetched.name == "Muhammad Ali"

def test_get_boxer_by_id_not_found(app):
    """Test error when fetching nonexistent boxer by ID."""
    with pytest.raises(ValueError, match="not found"):
        Boxers.get_boxer_by_id(999)


def test_get_boxer_by_name(boxer_tyson):
    """Test fetching a boxer by name."""
    fetched = Boxers.get_boxer_by_name("Mike Tyson")
    assert fetched.id == boxer_tyson.id

def test_get_boxer_by_name_not_found(app):
    """Test error when fetching nonexistent boxer by name."""
    with pytest.raises(ValueError, match="not found"):
        Boxers.get_boxer_by_name("Ghost Boxer")


# --- Delete Boxer ---

def test_delete_boxer_by_id(session, boxer_ali):
    """Test deleting a boxer by ID."""
    Boxers.delete(boxer_ali.id)
    assert session.query(Boxers).get(boxer_ali.id) is None

def test_delete_boxer_not_found(app):
    """Test deleting a non-existent boxer by ID."""
    with pytest.raises(ValueError, match="not found"):
        Boxers.delete(999)


# --- Stats Update ---

def test_update_stats_win_loss(session, boxer_ali):
    """Test updating stats for both win and loss."""
    boxer_ali.update_stats("win")
    assert boxer_ali.fights == 1
    assert boxer_ali.wins == 1

    boxer_ali.update_stats("loss")
    assert boxer_ali.fights == 2
    assert boxer_ali.wins == 1


def test_update_stats_invalid_result(boxer_ali):
    """Test stat update with invalid result type."""
    with pytest.raises(ValueError, match="Result must be 'win' or 'loss'"):
        boxer_ali.update_stats("draw")


# --- Weight Class ---

@pytest.mark.parametrize("weight,expected_class", [
    (210, "HEAVYWEIGHT"),
    (180, "MIDDLEWEIGHT"),
    (140, "LIGHTWEIGHT"),
    (125, "FEATHERWEIGHT"),
])
def test_weight_class_valid(weight, expected_class):
    """Test weight class calculation using valid weights."""
    assert Boxers.get_weight_class(weight) == expected_class

@pytest.mark.parametrize("weight", [0, 100, 124])
def test_weight_class_invalid(weight):
    """Test invalid weights raise ValueError."""
    with pytest.raises(ValueError, match="Invalid weight"):
        Boxers.get_weight_class(weight)


# --- Leaderboard ---

def test_leaderboard_wins(session, boxer_ali, boxer_tyson):
    """Test leaderboard sorting by win count."""
    boxer_ali.fights = 10
    boxer_ali.wins = 8
    boxer_tyson.fights = 10
    boxer_tyson.wins = 5
    session.commit()

    leaderboard = Boxers.get_leaderboard(sort_by="wins")
    assert leaderboard[0]["name"] == "Muhammad Ali"
    assert leaderboard[1]["name"] == "Mike Tyson"


def test_leaderboard_win_pct(session, boxer_ali, boxer_tyson):
    """Test leaderboard sorting by win percentage."""
    boxer_ali.fights = 10
    boxer_ali.wins = 6
    boxer_tyson.fights = 6
    boxer_tyson.wins = 5
    session.commit()

    leaderboard = Boxers.get_leaderboard(sort_by="win_pct")
    assert leaderboard[0]["name"] == "Mike Tyson"
    assert leaderboard[1]["name"] == "Muhammad Ali"


def test_leaderboard_invalid_sort():
    """Test leaderboard with invalid sort key."""
    with pytest.raises(ValueError, match="Invalid sort_by"):
        Boxers.get_leaderboard(sort_by="invalid")
>>>>>>> upstream/solutions
