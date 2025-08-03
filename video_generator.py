"""
Video Generator

High-level interface for generating AI advertisement videos using the Captions API.
"""

import os
import time
from datetime import datetime
from typing import Optional, Dict, Any
from urllib.parse import urlparse
import logging

from captions_api import CaptionsAPIClient, CaptionsAPIError

logger = logging.getLogger(__name__)


class VideoGenerator:
    """High-level interface for generating AI advertisement videos."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the video generator.
        
        Args:
            api_key: Captions API key. If not provided, will use environment variable.
        """
        self.client = CaptionsAPIClient(api_key)
    
    def generate_ad_video(
        self,
        script: str,
        creator_name: str,
        media_urls: list = None,
        resolution: str = "fhd",
        webhook_id: str = None,
        output_dir: str = "./generated_videos",
        filename: Optional[str] = None
    ) -> str:
        """
        Generate an AI advertisement video.
        
        Args:
            script: The script for the advertisement
            creator_name: Name of the AI creator to use
            media_urls: List of media URLs to include in the video
            resolution: Video resolution (default: "fhd")
            output_dir: Directory to save the generated video
            filename: Custom filename for the video (optional)
            
        Returns:
            Path to the generated video file
            
        Raises:
            CaptionsAPIError: If video generation fails
        """
        # Validate inputs
        self._validate_inputs(script, creator_name, resolution)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename if not provided
        if not filename:
            filename = self._generate_filename(script, creator_name, resolution)
        
        output_path = os.path.join(output_dir, filename)
        
        try:
            # Create the AI ad job
            operation_id = self.client.create_ai_ad(script, creator_name, media_urls, resolution, webhook_id)
            
            # Wait for completion
            video_url = self.client.wait_for_completion(operation_id)
            
            # Download the video
            final_path = self.client.download_video(video_url, output_path)
            
            logger.info(f"Video generation completed successfully: {final_path}")
            return final_path
            
        except CaptionsAPIError as e:
            logger.error(f"Video generation failed: {str(e)}")
            raise
    
    def _validate_inputs(self, script: str, creator_name: str, resolution: str):
        """Validate input parameters."""
        # Validate script
        if not script or len(script.strip()) < 10:
            raise CaptionsAPIError("Script must be at least 10 characters long")
        
        # Validate creator name
        if not creator_name or len(creator_name.strip()) < 1:
            raise CaptionsAPIError("Creator name is required")
        
        # Validate resolution
        valid_resolutions = ["fhd", "hd", "4k"]
        if resolution.lower() not in valid_resolutions:
            raise CaptionsAPIError(f"Invalid resolution. Must be one of: {', '.join(valid_resolutions)}")
    
    def _check_credits(self, duration: int):
        """Check if user has sufficient credits for the video generation."""
        # Credits endpoint doesn't exist in the current API
        logger.info("Skipping credits check - endpoint not available in current API")
    
    def _generate_filename(self, script: str, creator_name: str, resolution: str) -> str:
        """Generate a filename for the video based on script and parameters."""
        # Create timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Generate filename
        filename = f"ai_ad_{creator_name}_{resolution}_{timestamp}.mp4"
        
        # Clean filename (remove invalid characters)
        filename = "".join(c for c in filename if c.isalnum() or c in "._-")
        
        return filename
    
    def get_generation_status(self, operation_id: str) -> Dict[str, Any]:
        """
        Get the status of a video generation job.
        
        Args:
            operation_id: The operation ID to check
            
        Returns:
            Job status information
        """
        return self.client.get_job_status(operation_id)
    
    def list_creators(self) -> Dict[str, Any]:
        """
        Get a list of available AI creators.
        
        Returns:
            List of supported creators
        """
        return self.client.list_creators() 