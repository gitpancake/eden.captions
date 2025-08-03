"""
Captions API Client

A Python client for the Captions AI Ads API that handles video generation,
status checking, and file downloads.
"""

import os
import time
import requests
from typing import Dict, Optional, Any
from urllib.parse import urljoin
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CaptionsAPIError(Exception):
    """Custom exception for Captions API errors."""
    pass


class CaptionsAPIClient:
    """Client for interacting with the Captions AI Ads API."""
    
    BASE_URL = "https://api.captions.ai"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Captions API client.
        
        Args:
            api_key: API key for authentication. If not provided, will try to get from environment.
        """
        self.api_key = api_key or os.getenv("CAPTIONS_API_KEY")
        if not self.api_key:
            raise CaptionsAPIError("API key is required. Set CAPTIONS_API_KEY environment variable or pass api_key parameter.")
        
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": self.api_key,
            "Content-Type": "application/json",
            "User-Agent": "CaptionsAI-Python-Client/1.0"
        })
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """
        Make an HTTP request to the Captions API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests
            
        Returns:
            API response as dictionary
            
        Raises:
            CaptionsAPIError: If the request fails
        """
        url = urljoin(self.BASE_URL, endpoint)
        
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise CaptionsAPIError("Invalid API key. Please check your credentials.")
            elif e.response.status_code == 429:
                raise CaptionsAPIError("Rate limit exceeded. Please wait before making another request.")
            elif e.response.status_code == 402:
                raise CaptionsAPIError("Insufficient credits. Please purchase more credits.")
            elif e.response.status_code == 400:
                try:
                    error_detail = e.response.json()
                    raise CaptionsAPIError(f"Bad request: {error_detail}")
                except:
                    raise CaptionsAPIError(f"Bad request: {e.response.text}")
            else:
                raise CaptionsAPIError(f"API request failed: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise CaptionsAPIError(f"API request failed: {str(e)}")
    
    def create_ai_ad(self, script: str, creator_name: str, media_urls: list = None, resolution: str = "fhd", webhook_id: str = None) -> str:
        """
        Create an AI-generated advertisement video.
        
        Args:
            script: The script for the advertisement
            creator_name: Name of the AI creator to use
            media_urls: List of media URLs to include in the video
            resolution: Video resolution (default: "fhd")
            
        Returns:
            Operation ID for tracking the video generation progress
        """
        endpoint = "/api/ads/submit"
        
        # Ensure we have at least one media URL (required by API)
        if not media_urls:
            media_urls = ["https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=800&h=600&fit=crop"]
        
        payload = {
            "script": script,
            "creatorName": creator_name,
            "mediaUrls": media_urls,
            "resolution": resolution
        }
        
        if webhook_id:
            payload["webhookId"] = webhook_id
        
        # Remove None values to avoid API issues
        payload = {k: v for k, v in payload.items() if v is not None}
        
        logger.info(f"Creating AI ad with creator: {creator_name}")
        logger.info(f"Payload: {payload}")
        response = self._make_request("POST", endpoint, json=payload)
        
        operation_id = response.get("operationId")
        if not operation_id:
            raise CaptionsAPIError("No operation ID received from API")
        
        logger.info(f"AI ad job created with operation ID: {operation_id}")
        return operation_id
    
    def get_job_status(self, operation_id: str) -> Dict[str, Any]:
        """
        Get the status of a video generation job.
        
        Args:
            operation_id: The operation ID returned from create_ai_ad
            
        Returns:
            Job status information including state and video URL if complete
        """
        endpoint = "/api/ads/poll"
        
        payload = {
            "operationId": operation_id
        }
        
        response = self._make_request("POST", endpoint, json=payload)
        return response
    
    def wait_for_completion(self, operation_id: str, timeout: int = 300, poll_interval: int = 10) -> str:
        """
        Wait for a video generation job to complete.
        
        Args:
            operation_id: The operation ID to wait for
            timeout: Maximum time to wait in seconds (default: 300)
            poll_interval: Time between status checks in seconds (default: 10)
            
        Returns:
            URL of the completed video
            
        Raises:
            CaptionsAPIError: If the job fails or times out
        """
        start_time = time.time()
        
        while True:
            if time.time() - start_time > timeout:
                raise CaptionsAPIError(f"Job {operation_id} timed out after {timeout} seconds")
            
            status = self.get_job_status(operation_id)
            state = status.get("state", "unknown")
            
            logger.info(f"Job {operation_id} status: {state}")
            
            if state == "COMPLETE":
                video_url = status.get("url")
                if video_url:
                    logger.info(f"Video generation completed: {video_url}")
                    return video_url
                else:
                    raise CaptionsAPIError("Job completed but no video URL found")
            
            elif state == "FAILED":
                error = status.get("error", "Unknown error")
                raise CaptionsAPIError(f"Job {operation_id} failed: {error}")
            
            elif state in ["PENDING", "PROCESSING", "QUEUED"]:
                time.sleep(poll_interval)
                continue
            
            else:
                raise CaptionsAPIError(f"Unknown job state: {state}")
    
    def download_video(self, video_url: str, output_path: str) -> str:
        """
        Download a video from the provided URL.
        
        Args:
            video_url: URL of the video to download
            output_path: Local path where the video should be saved
            
        Returns:
            Path to the downloaded video file
        """
        try:
            logger.info(f"Downloading video to: {output_path}")
            response = self.session.get(video_url, stream=True)
            response.raise_for_status()
            
            # Ensure output directory exists
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Video downloaded successfully: {output_path}")
            return output_path
            
        except requests.exceptions.RequestException as e:
            raise CaptionsAPIError(f"Failed to download video: {str(e)}")
    
    def list_creators(self) -> Dict[str, Any]:
        """
        Get a list of available AI creators for ad generation.
        
        Returns:
            List of supported creators and their thumbnails
        """
        endpoint = "/api/ads/list-creators"
        return self._make_request("POST", endpoint) 