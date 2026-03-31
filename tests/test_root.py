"""
Tests for the root endpoint (GET /)

This module tests the root endpoint which redirects to the static index.html file.
"""

import pytest


class TestRootEndpoint:
    """Tests for GET / endpoint"""

    def test_root_redirects_to_static_index(self, client, reset_activities):
        """
        Test that root endpoint redirects to /static/index.html
        
        Verifies that GET / returns a 307 (temporary) redirect status code
        pointing to the static index.html file.
        
        AAA Pattern:
        - Arrange: Client is ready (from fixture)
        - Act: Make GET request to root endpoint
        - Assert: Verify 307 redirect status and location header
        """
        # ========== ARRANGE ==========
        # Client provided by fixture, no additional setup needed
        
        # ========== ACT ==========
        response = client.get("/", follow_redirects=False)
        
        # ========== ASSERT ==========
        assert response.status_code == 307, "Expected temporary redirect (307) status code"
        assert response.headers.get("location") == "/static/index.html", \
            "Expected redirect to /static/index.html"
