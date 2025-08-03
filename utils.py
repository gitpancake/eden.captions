"""
Utility functions for the Captions AI Ads Generator.

Helper functions for file operations, URL validation, and other common tasks.
"""

import os
import re
from typing import Optional, List
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)


def validate_url(url: str) -> bool:
    """
    Validate if a string is a proper URL.
    
    Args:
        url: URL string to validate
        
    Returns:
        True if valid URL, False otherwise
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def sanitize_filename(filename: str) -> str:
    """
    Sanitize a filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename safe for file system
    """
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure filename is not empty
    if not filename:
        filename = "unnamed_file"
    
    return filename


def ensure_directory_exists(directory_path: str) -> str:
    """
    Ensure a directory exists, creating it if necessary.
    
    Args:
        directory_path: Path to the directory
        
    Returns:
        Absolute path to the directory
    """
    abs_path = os.path.abspath(directory_path)
    os.makedirs(abs_path, exist_ok=True)
    return abs_path


def get_file_size_mb(file_path: str) -> Optional[float]:
    """
    Get file size in megabytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in MB, or None if file doesn't exist
    """
    try:
        if os.path.exists(file_path):
            size_bytes = os.path.getsize(file_path)
            return size_bytes / (1024 * 1024)  # Convert to MB
        return None
    except Exception as e:
        logger.warning(f"Could not get file size for {file_path}: {e}")
        return None


def format_duration(seconds: int) -> str:
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string (e.g., "2m 30s")
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        if remaining_seconds == 0:
            return f"{minutes}m"
        else:
            return f"{minutes}m {remaining_seconds}s"
    else:
        hours = seconds // 3600
        remaining_minutes = (seconds % 3600) // 60
        remaining_seconds = seconds % 60
        if remaining_seconds == 0 and remaining_minutes == 0:
            return f"{hours}h"
        elif remaining_seconds == 0:
            return f"{hours}h {remaining_minutes}m"
        else:
            return f"{hours}h {remaining_minutes}m {remaining_seconds}s"


def format_file_size(size_mb: float) -> str:
    """
    Format file size in MB to human-readable string.
    
    Args:
        size_mb: File size in megabytes
        
    Returns:
        Formatted file size string (e.g., "15.2 MB")
    """
    if size_mb < 1:
        return f"{size_mb * 1024:.1f} KB"
    elif size_mb < 1024:
        return f"{size_mb:.1f} MB"
    else:
        return f"{size_mb / 1024:.1f} GB"


def extract_domain_from_url(url: str) -> str:
    """
    Extract domain name from URL.
    
    Args:
        url: URL string
        
    Returns:
        Domain name without www prefix
    """
    try:
        domain = urlparse(url).netloc
        return domain.replace("www.", "")
    except Exception:
        return "unknown"


def list_generated_videos(directory: str) -> List[str]:
    """
    List all generated video files in a directory.
    
    Args:
        directory: Directory to search
        
    Returns:
        List of video file paths
    """
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm'}
    video_files = []
    
    try:
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    _, ext = os.path.splitext(filename)
                    if ext.lower() in video_extensions:
                        video_files.append(file_path)
    except Exception as e:
        logger.warning(f"Could not list videos in {directory}: {e}")
    
    return sorted(video_files, key=os.path.getmtime, reverse=True)


def calculate_credits_cost(duration_seconds: int) -> float:
    """
    Calculate the cost in credits for a video of given duration.
    
    Args:
        duration_seconds: Video duration in seconds
        
    Returns:
        Cost in credits (1 credit per second)
    """
    return float(duration_seconds)


def calculate_credits_cost_usd(duration_seconds: int) -> float:
    """
    Calculate the cost in USD for a video of given duration.
    
    Args:
        duration_seconds: Video duration in seconds
        
    Returns:
        Cost in USD (1 credit = $0.05)
    """
    credits = calculate_credits_cost(duration_seconds)
    return credits * 0.05 