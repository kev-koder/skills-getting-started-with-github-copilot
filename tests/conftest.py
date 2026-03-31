"""
Pytest configuration and shared fixtures for Mergington High School API tests.

This module provides:
- TestClient fixture for making HTTP requests to the FastAPI app
- Mock activities data fixture that resets state between tests
- Utility fixtures for test data (emails, activity names, etc.)
"""

import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """
    Fixture providing a TestClient for the FastAPI application.
    
    The TestClient allows synchronous testing of async FastAPI endpoints.
    Each test receives a fresh client instance.
    
    Yields:
        TestClient: A test client for making requests to the app
    """
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """
    Fixture that resets the activities dictionary to its default state.
    
    This ensures each test starts with a clean, known state of activities
    and their participant lists. Runs before each test and cleans up after.
    
    The fixture uses copy.deepcopy() to ensure nested structures (participant
    lists) are properly reset.
    
    Yields:
        None
    """
    # Store original activities state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team for intramural and regional tournaments",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and participate in friendly matches",
            "schedule": "Saturdays, 10:00 AM - 12:00 PM",
            "max_participants": 16,
            "participants": ["jessica@mergington.edu", "ryan@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and develop acting skills",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["maya@mergington.edu", "lucas@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media art techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["sophia@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills through competitive debate",
            "schedule": "Mondays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["marcus@mergington.edu", "anna@mergington.edu", "david@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and explore advanced scientific concepts",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["priya@mergington.edu"]
        }
    }
    
    # Before test: make sure app state is clean
    activities.clear()
    activities.update(copy.deepcopy(original_activities))
    
    yield
    
    # After test: reset for next test
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


@pytest.fixture
def test_email():
    """
    Fixture providing a test email address for signup tests.
    
    Returns:
        str: A test email address (test.student@mergington.edu)
    """
    return "test.student@mergington.edu"


@pytest.fixture
def activity_name():
    """
    Fixture providing a valid activity name for tests.
    
    Returns:
        str: The name "Chess Club" (a valid activity from the app)
    """
    return "Chess Club"


@pytest.fixture
def invalid_activity_name():
    """
    Fixture providing an invalid activity name (does not exist).
    
    Returns:
        str: A non-existent activity name for 404 error testing
    """
    return "Nonexistent Activity"
