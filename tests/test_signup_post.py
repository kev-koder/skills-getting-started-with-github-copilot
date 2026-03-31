"""
Tests for student signup endpoint (POST /activities/{activity_name}/signup)

This module tests registration of students for activities.
"""

import pytest


class TestSignupPostEndpoint:
    """Tests for POST /activities/{activity_name}/signup endpoint"""

    def test_student_signup_success(self, client, reset_activities, activity_name, test_email):
        """
        Test that a student can successfully sign up for an activity
        
        Verifies that a new student can be added to an activity's participant
        list and receives a success message.
        
        AAA Pattern:
        - Arrange: Reset activities, prepare test email and activity
        - Act: POST signup request with activity name and email
        - Assert: Verify 200 status and success message
        """
        # ========== ARRANGE ==========
        # Activity and email provided by fixtures
        # Initial state: test_email is not yet signed up
        
        # ========== ACT ==========
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": test_email}
        )
        
        # ========== ASSERT ==========
        assert response.status_code == 200, "Expected 200 OK status code"
        assert "Signed up" in response.json()["message"], \
            "Expected success message containing 'Signed up'"
        assert test_email in response.json()["message"], \
            f"Expected email {test_email} in response message"

    def test_student_appears_in_activity_after_signup(self, client, reset_activities, activity_name, test_email):
        """
        Test that student appears in activity participant list after signup
        
        Verifies that after signup, the student email is added to the
        activity's participants list.
        
        AAA Pattern:
        - Arrange: Verify test_email not in Chess Club initially
        - Act: Sign up student, then retrieve activities
        - Assert: Verify test_email is now in participants
        """
        # ========== ARRANGE ==========
        response_initial = client.get("/activities")
        initial_participants = response_initial.json()[activity_name]["participants"]
        assert test_email not in initial_participants, \
            f"Test email should not be in {activity_name} initially"
        
        # ========== ACT ==========
        client.post(f"/activities/{activity_name}/signup", params={"email": test_email})
        response_after = client.get("/activities")
        
        # ========== ASSERT ==========
        updated_participants = response_after.json()[activity_name]["participants"]
        assert test_email in updated_participants, \
            f"Test email should be in participants after signup"

    def test_multiple_students_signup_to_same_activity(self, client, reset_activities, activity_name):
        """
        Test that multiple students can sign up for the same activity
        
        Verifies that multiple different students can be added to
        the same activity without conflicts.
        
        AAA Pattern:
        - Arrange: Prepare two unique test emails
        - Act: Sign up both students to the same activity
        - Assert: Verify both are in participant list
        """
        # ========== ARRANGE ==========
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # ========== ACT ==========
        response1 = client.post(f"/activities/{activity_name}/signup", params={"email": email1})
        response2 = client.post(f"/activities/{activity_name}/signup", params={"email": email2})
        response_activities = client.get("/activities")
        
        # ========== ASSERT ==========
        assert response1.status_code == 200, "First student signup should succeed"
        assert response2.status_code == 200, "Second student signup should succeed"
        participants = response_activities.json()[activity_name]["participants"]
        assert email1 in participants, "First email should be in participants"
        assert email2 in participants, "Second email should be in participants"

    def test_signup_for_nonexistent_activity_returns_404(self, client, reset_activities, test_email, invalid_activity_name):
        """
        Test that signing up for nonexistent activity returns 404 error
        
        Verifies that attempting to signup for an activity that does not
        exist returns a 404 Not Found error.
        
        AAA Pattern:
        - Arrange: Use invalid_activity_name that doesn't exist
        - Act: Attempt GET request with invalid activity name
        - Assert: Verify 404 status and activity not found message
        """
        # ========== ARRANGE ==========
        # invalid_activity_name is provided by fixture
        
        # ========== ACT ==========
        response = client.post(
            f"/activities/{invalid_activity_name}/signup",
            params={"email": test_email}
        )
        
        # ========== ASSERT ==========
        assert response.status_code == 404, "Expected 404 Not Found status code"
        assert "Activity not found" in response.json()["detail"], \
            "Expected 'Activity not found' in error message"

    def test_duplicate_signup_returns_400(self, client, reset_activities, activity_name):
        """
        Test that student cannot sign up twice for the same activity
        
        Verifies that attempting to signup with an email already registered
        returns a 400 Bad Request error with appropriate message.
        
        AAA Pattern:
        - Arrange: Use email that's already in Chess Club (michael@mergington.edu)
        - Act: Attempt to signup with existing participant email
        - Assert: Verify 400 status and duplicate signup message
        """
        # ========== ARRANGE ==========
        # michael@mergington.edu is already in Chess Club from default data
        existing_email = "michael@mergington.edu"
        
        # ========== ACT ==========
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # ========== ASSERT ==========
        assert response.status_code == 400, "Expected 400 Bad Request status code"
        assert "already signed up" in response.json()["detail"], \
            "Expected 'already signed up' in error message"
