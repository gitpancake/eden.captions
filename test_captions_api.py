#!/usr/bin/env python3
"""
Test script for Captions API functionality

This script tests the API client without making actual API calls.
"""

import unittest
from unittest.mock import Mock, patch
import tempfile
import os

from captions_api import CaptionsAPIClient, CaptionsAPIError
from video_generator import VideoGenerator
from utils import validate_url, format_duration, format_file_size


class TestCaptionsAPI(unittest.TestCase):
    """Test cases for Captions API client."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test_api_key_123"
        self.client = CaptionsAPIClient(self.api_key)
    
    def test_init_with_api_key(self):
        """Test client initialization with API key."""
        client = CaptionsAPIClient(self.api_key)
        self.assertEqual(client.api_key, self.api_key)
        self.assertIn("Authorization", client.session.headers)
    
    def test_init_without_api_key(self):
        """Test client initialization without API key raises error."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(CaptionsAPIError):
                CaptionsAPIClient()
    
    def test_make_request_success(self):
        """Test successful API request."""
        mock_response = Mock()
        mock_response.json.return_value = {"job_id": "test_job_123"}
        mock_response.raise_for_status.return_value = None
        
        with patch.object(self.client.session, 'request', return_value=mock_response):
            result = self.client._make_request("POST", "/test", json={"test": "data"})
            self.assertEqual(result, {"job_id": "test_job_123"})
    
    def test_make_request_401_error(self):
        """Test API request with 401 error."""
        from requests.exceptions import HTTPError
        
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = HTTPError("401")
        
        with patch.object(self.client.session, 'request', return_value=mock_response):
            with self.assertRaises(CaptionsAPIError) as context:
                self.client._make_request("POST", "/test")
            self.assertIn("Invalid API key", str(context.exception))
    
    def test_make_request_429_error(self):
        """Test API request with 429 error."""
        from requests.exceptions import HTTPError
        
        mock_response = Mock()
        mock_response.status_code = 429
        mock_response.raise_for_status.side_effect = HTTPError("429")
        
        with patch.object(self.client.session, 'request', return_value=mock_response):
            with self.assertRaises(CaptionsAPIError) as context:
                self.client._make_request("POST", "/test")
            self.assertIn("Rate limit exceeded", str(context.exception))


class TestVideoGenerator(unittest.TestCase):
    """Test cases for Video Generator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = VideoGenerator("test_api_key")
    
    def test_validate_inputs_valid(self):
        """Test input validation with valid inputs."""
        try:
            self.generator._validate_inputs(
                "https://example.com/product",
                30,
                "professional"
            )
        except CaptionsAPIError:
            self.fail("Valid inputs should not raise an error")
    
    def test_validate_inputs_invalid_url(self):
        """Test input validation with invalid URL."""
        with self.assertRaises(CaptionsAPIError):
            self.generator._validate_inputs("invalid-url", 30, "professional")
    
    def test_validate_inputs_invalid_duration(self):
        """Test input validation with invalid duration."""
        with self.assertRaises(CaptionsAPIError):
            self.generator._validate_inputs(
                "https://example.com/product",
                200,  # Too long
                "professional"
            )
    
    def test_validate_inputs_invalid_style(self):
        """Test input validation with invalid style."""
        with self.assertRaises(CaptionsAPIError):
            self.generator._validate_inputs(
                "https://example.com/product",
                30,
                "invalid_style"
            )
    
    def test_generate_filename(self):
        """Test filename generation."""
        filename = self.generator._generate_filename(
            "https://www.apple.com/iphone-15/",
            30,
            "professional"
        )
        
        self.assertIn("ai_ad_", filename)
        self.assertIn("apple.com", filename)
        self.assertIn("professional", filename)
        self.assertIn("30s", filename)
        self.assertIn(".mp4", filename)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_validate_url_valid(self):
        """Test URL validation with valid URLs."""
        valid_urls = [
            "https://example.com",
            "http://www.test.com/path",
            "https://api.example.com/v1/endpoint"
        ]
        
        for url in valid_urls:
            self.assertTrue(validate_url(url), f"URL should be valid: {url}")
    
    def test_validate_url_invalid(self):
        """Test URL validation with invalid URLs."""
        invalid_urls = [
            "not-a-url",
            "example.com",
            ""
        ]
        
        for url in invalid_urls:
            self.assertFalse(validate_url(url), f"URL should be invalid: {url}")
    
    def test_format_duration(self):
        """Test duration formatting."""
        test_cases = [
            (30, "30s"),
            (90, "1m 30s"),
            (3600, "1h"),
            (3661, "1h 1m 1s")
        ]
        
        for seconds, expected in test_cases:
            result = format_duration(seconds)
            self.assertEqual(result, expected)
    
    def test_format_file_size(self):
        """Test file size formatting."""
        test_cases = [
            (0.5, "512.0 KB"),
            (1.5, "1.5 MB"),
            (1024, "1.0 GB")
        ]
        
        for size_mb, expected in test_cases:
            result = format_file_size(size_mb)
            self.assertEqual(result, expected)


if __name__ == "__main__":
    # Run tests
    unittest.main(verbosity=2) 