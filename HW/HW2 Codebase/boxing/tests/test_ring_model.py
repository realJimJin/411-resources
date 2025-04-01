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

