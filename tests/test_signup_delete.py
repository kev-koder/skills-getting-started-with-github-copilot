"""
Tests for student unregistration endpoint (DELETE /activities/{activity_name}/signup)

This module tests removal of students from activities.
"""

import pytest


class TestSignupDeleteEndpoint:
    """Tests for DELETE /activities/{activity_name}/signup endpoint"""

    def test_student_unregister_success(self, client, reset_activities, activity_name):
        """
        Test that a student can successfully unregister from an activity
        
        Verifies that an existing participant can be removed from an activity
        and receives a success message.
        
        AAA Pattern:
        - Arrange: Use email already in Chess Club (michael@mergington.edu)
        - Act: DELETE request to unregister from activity
        - Assert: Verify 200 status and success message
        """
        # ========== ARRANGE ==========
        # michael@mergington.edu is already in Chess Club from default data
        existing_email = "michael@mergington.edu"
        
        # ========== ACT ==========
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # ========== ASSERT ==========
        assert response.status_code == 200, "Expected 200 OK status code"
        assert "Unregistered" in response.json()["message"], \
            "Expected success message containing 'Unregistered'"
        assert existing_email in response.json()["message"], \
            f"Expected email {existing_email} in response message"

    def test_student_removed_from_participants_after_unregister(self, client, reset_activities, activity_name):
        """
        Test that student is removed from participant list after unregister
        
        Verifies that after unregistering, the student email is no longer
        in the activity's participants list.
        
        AAA Pattern:
        - Arrange: Verify michael@mergington.edu is in Chess Club initially
        - Act: Unregister michael@mergington.edu, retrieve activities
        - Assert: Verify michael@mergington.edu is no longer in participants
        """
        # ========== ARRANGE ==========
        existing_email = "michael@mergington.edu"
        response_initial = client.get("/activities")
        initial_participants = response_initial.json()[activity_name]["participants"]
        assert existing_email in initial_participants, \
            f"Expected {existing_email} in participants initially"
        
        # ========== ACT ==========
        client.delete(f"/activities/{activity_name}/signup", params={"email": existing_email})
        response_after = client.get("/activities")
        
        # ========== ASSERT ==========
        updated_participants = response_after.json()[activity_name]["participants"]
        assert existing_email not in updated_participants, \
            f"Expected {existing_email} to be removed from participants"

    def test_unregister_from_nonexistent_activity_returns_404(self, client, reset_activities, test_email, invalid_activity_name):
        """
        Test that unregistering from nonexistent activity returns 404 error
        
        Verifies that attempting to unregister from an activity that does not
        exist returns a 404 Not Found error.
        
        AAA Pattern:
        - Arrange: Use invalid_activity_name that doesn't exist
        - Act: DELETE request with invalid activity name
        - Assert: Verify 404 status and activity not found message
        """
        # ========== ARRANGE ==========
        # invalid_activity_name is provided by fixture
        
        # ========== ACT ==========
        response = client.delete(
            f"/activities/{invalid_activity_name}/signup",
            params={"email": test_email}
        )
        
        # ========== ASSERT ==========
        assert response.status_code == 404, "Expected 404 Not Found status code"
        assert "Activity not found" in response.json()["detail"], \
            "Expected 'Activity not found' in error message"

    def test_unregister_non_participant_returns_400(self, client, reset_activities, activity_name, test_email):
        """
        Test that unregistering non-participant returns 400 error
        
        Verifies that attempting to unregister someone who is not signed up
        returns a 400 Bad Request error with appropriate message.
        
        AAA Pattern:
        - Arrange: Use test_email not in any activity
        - Act: Attempt to DELETE with email not in participants
        - Assert: Verify 400 status and not signed up message
        """
        # ========== ARRANGE ==========
        # test_email (test.student@mergington.edu) is not in Chess Club
        response_initial = client.get("/activities")
        participants = response_initial.json()[activity_name]["participants"]
        assert test_email not in participants, \
            f"Test email should not be in {activity_name} participants"
        
        # ========== ACT ==========
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        
        # ========== ASSERT ==========
        assert response.status_code == 400, "Expected 400 Bad Request status code"
        assert "not signed up" in response.json()["detail"], \
            "Expected 'not signed up' in error message"

    def test_unregister_only_participant_succeeds(self, client, reset_activities):
        """
        Test that unregistering the only participant from an activity succeeds
        
        Verifies that an activity can have all participants removed, leaving
        an empty participant list.
        
        AAA Pattern:
        - Arrange: Identify activity with single participant (Basketball Team)
        - Act: Unregister the only participant
        - Assert: Verify success and empty participants list
        """
        # ========== ARRANGE ==========
        # Basketball Team has one participant: alex@mergington.edu
        activity = "Basketball Team"
        sole_participant = "alex@mergington.edu"
        
        response_initial = client.get("/activities")
        initial_participants = response_initial.json()[activity]["participants"]
        assert len(initial_participants) == 1, \
            f"Expected {activity} to have exactly 1 participant"
        assert sole_participant in initial_participants, \
            f"Expected {sole_participant} in {activity}"
        
        # ========== ACT ==========
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": sole_participant}
        )
        response_after = client.get("/activities")
        
        # ========== ASSERT ==========
        assert response.status_code == 200, "Expected 200 OK status code"
        updated_participants = response_after.json()[activity]["participants"]
        assert len(updated_participants) == 0, \
            "Expected empty participants list after unregistering sole participant"
