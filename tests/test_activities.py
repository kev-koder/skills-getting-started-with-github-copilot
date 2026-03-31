"""
Tests for the activities list endpoint (GET /activities)

This module tests retrieval of all activities from the API.
"""

import pytest


class TestActivitiesEndpoint:
    """Tests for GET /activities endpoint"""

    def test_get_all_activities_returns_dict(self, client, reset_activities):
        """
        Test that GET /activities returns all activities as a dictionary
        
        Verifies the endpoint returns HTTP 200 with activities data
        in dictionary format.
        
        AAA Pattern:
        - Arrange: Reset activities to known state via fixture
        - Act: Make GET request to /activities endpoint
        - Assert: Verify 200 status and response is a dict
        """
        # ========== ARRANGE ==========
        # Activities reset to default state via fixture
        
        # ========== ACT ==========
        response = client.get("/activities")
        
        # ========== ASSERT ==========
        assert response.status_code == 200, "Expected 200 OK status code"
        assert isinstance(response.json(), dict), "Expected response to be a dictionary"

    def test_get_activities_contains_all_nine_activities(self, client, reset_activities):
        """
        Test that GET /activities returns all nine default activities
        
        Verifies the response contains the complete list of activities
        defined in the application.
        
        AAA Pattern:
        - Arrange: Reset activities to known state
        - Act: Get activities from endpoint
        - Assert: Verify all 9 activities are present
        """
        # ========== ARRANGE ==========
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Drama Club",
            "Art Studio",
            "Debate Team",
            "Science Club"
        ]
        
        # ========== ACT ==========
        response = client.get("/activities")
        activities_data = response.json()
        
        # ========== ASSERT ==========
        assert len(activities_data) == 9, "Expected exactly 9 activities"
        for activity_name in expected_activities:
            assert activity_name in activities_data, \
                f"Expected activity '{activity_name}' not found in response"

    def test_activity_structure_has_required_fields(self, client, reset_activities):
        """
        Test that each activity has the required fields
        
        Verifies each activity object contains description, schedule,
        max_participants, and participants fields.
        
        AAA Pattern:
        - Arrange: List of required field names
        - Act: Get activities and check first activity structure
        - Assert: Verify all required fields are present
        """
        # ========== ARRANGE ==========
        required_fields = {
            "description",
            "schedule",
            "max_participants",
            "participants"
        }
        
        # ========== ACT ==========
        response = client.get("/activities")
        activities_data = response.json()
        # Check the first activity (Chess Club)
        chess_club = activities_data.get("Chess Club")
        
        # ========== ASSERT ==========
        assert chess_club is not None, "Chess Club not found"
        activity_fields = set(chess_club.keys())
        assert activity_fields == required_fields, \
            f"Activity fields {activity_fields} do not match required {required_fields}"

    def test_participants_list_is_present_in_activities(self, client, reset_activities):
        """
        Test that activities with existing participants show correct list
        
        Verifies that the participants field contains the correct emails
        for activities that have participants.
        
        AAA Pattern:
        - Arrange: Expected participants for Chess Club
        - Act: Retrieve activities and get Chess Club data
        - Assert: Verify participant list matches expected
        """
        # ========== ARRANGE ==========
        expected_chess_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
        
        # ========== ACT ==========
        response = client.get("/activities")
        activities_data = response.json()
        chess_participants = activities_data["Chess Club"]["participants"]
        
        # ========== ASSERT ==========
        assert chess_participants == expected_chess_participants, \
            f"Expected {expected_chess_participants}, got {chess_participants}"
        assert len(chess_participants) == 2, "Expected 2 participants in Chess Club"
