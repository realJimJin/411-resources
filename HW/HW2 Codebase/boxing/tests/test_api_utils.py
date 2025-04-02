import pytest
import requests
from boxing.utils.api_utils import get_random


RANDOM_NUMBER = 0.42

@pytest.fixture
def mock_random_org(mocker):
    """Fixture to mock the random.org response."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = f"{RANDOM_NUMBER}\n"
    mocker.patch("requests.get", return_value=mock_response)
    return mock_response

def test_get_random_success(mock_random_org):
    """Test successful retrieval of a random number from random.org."""
    result = get_random()
    assert result == RANDOM_NUMBER, f"Expected {RANDOM_NUMBER}, got {result}"
    requests.get.assert_called_once_with(
        "https://www.random.org/decimal-fractions/?num=1&dec=2&col=1&format=plain&rnd=new",
        timeout=5
    )


def test_get_random_request_failure(mocker):
    """Test handling of a generic request failure."""
    mocker.patch("requests.get", side_effect=requests.exceptions.RequestException("Connection error"))

    with pytest.raises(RuntimeError, match="Request to random.org failed: Connection error"):
        get_random()


def test_get_random_timeout(mocker):
    """Test handling of a timeout."""
    mocker.patch("requests.get", side_effect=requests.exceptions.Timeout)

    with pytest.raises(RuntimeError, match="Request to random.org timed out."):
        get_random()


def test_get_random_invalid_response(mocker):
    """Test handling of an invalid response (non-float)."""
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.text = "not_a_number"
    mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(ValueError, match="Invalid response from random.org: not_a_number"):
        get_random()


def test_get_random_http_error(mocker):
    """Test handling of a failed HTTP status code."""
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
    mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(RuntimeError, match="Request to random.org failed: 500 Server Error"):
        get_random()