from dataclasses import asdict

import pytest 

from boxing.models.boxers_model import Boxer
from boxing.models.ring_model import RingModel

@pytest.fixture()
def ring_model():
    """Fixture to provide a new instance of RingModel for each test."""
    return RingModel()

@pytest.fixture
def mock_update_boxer_stats(mocker):
    """Mock the update_boxer_stats function for testing purposes."""
    return mocker.patch("boxer.models.ring_model.update_boxer_stats")

"""Fixtures providing sample boxers for the tests."""
@pytest.fixture
def sample_boxer1():
    return Boxer(1, 'Boxer 1', 130, 70, 13.5, 33)

@pytest.fixture
def sample_boxer2():
    return Boxer(2, 'Boxer 2', 130, 83, 15, 29)

@pytest.fixture
def sample_ring(sample_boxer1, sample_boxer2):
    return [sample_boxer1, sample_boxer2]

def test_enter_ring_valid_boxers(ring_model, sample_boxer1, sample_boxer2):
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)
    assert len(ring_model.ring) == 2

def test_enter_ring_invalid_type(ring_model):
    with pytest.raises(TypeError):
        ring_model.enter_ring("not_a_boxer")

def test_enter_ring_over_capacity(ring_model, sample_boxer1, sample_boxer2):
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)
    with pytest.raises(ValueError):
        ring_model.enter_ring(Boxer(3, 'Boxer 3', 120, 80, 12, 26))

def test_fight_too_few_boxers(ring_model, sample_boxer1):
    ring_model.enter_ring(sample_boxer1)
    with pytest.raises(ValueError):
        ring_model.fight()

def test_get_boxers_returns_boxers(ring_model, sample_boxer1):
    ring_model.enter_ring(sample_boxer1)
    boxers = ring_model.get_boxers()
    assert len(boxers) == 1
    assert boxers[0].name == 'Boxer 1'

def test_clear_ring(ring_model, sample_boxer1):
    ring_model.enter_ring(sample_boxer1)
    ring_model.clear_ring()
    assert ring_model.ring == []

def test_clear_ring_empty_raises(ring_model):
    with pytest.raises(ValueError):
        ring_model.clear_ring()

def test_get_fighting_skill(ring_model, sample_boxer1):
    skill = ring_model.get_fighting_skill(sample_boxer1)
    expected_skill = (130 * len(sample_boxer1.name)) + (sample_boxer1.reach / 10) + 0  # age = 33 -> 0
    assert skill == expected_skill

def test_fight_outcome_and_stat_update(ring_model, sample_boxer1, sample_boxer2, mocker):
    ring_model.enter_ring(sample_boxer1)
    ring_model.enter_ring(sample_boxer2)

    mock_update = mocker.patch("boxing.models.ring_model.update_boxer_stats")
    mock_random = mocker.patch("boxing.models.ring_model.get_random", return_value=0.9)

    winner = ring_model.fight()
    
    assert winner in [sample_boxer1.name, sample_boxer2.name]
    assert mock_update.call_count == 2  # one for winner, one for loser