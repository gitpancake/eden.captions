#!/usr/bin/env python3
"""
Captions AI Ads Generator - CLI Application

A command-line interface for generating AI-powered advertisement videos
using the Captions AI Ads API.
"""

import os
import sys
import json
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table
from rich.text import Text
from rich import print as rprint
from dotenv import load_dotenv

from video_generator import VideoGenerator
from captions_api import CaptionsAPIError
from utils import (
    validate_url, format_duration, format_file_size, 
    calculate_credits_cost_usd, list_generated_videos
)

# Load environment variables
load_dotenv()

# Initialize Rich console
console = Console()


def print_banner():
    """Print the application banner."""
    banner = """
    🎬 Captions AI Ads Generator 🎬
    
    Generate professional advertisement videos from product URLs
    using the power of AI.
    """
    console.print(Panel(banner, style="bold blue"))


def print_error(message: str):
    """Print an error message with consistent styling."""
    console.print(f"[bold red]❌ Error:[/bold red] {message}")


def print_success(message: str):
    """Print a success message with consistent styling."""
    console.print(f"[bold green]✅ Success:[/bold green] {message}")


def print_info(message: str):
    """Print an info message with consistent styling."""
    console.print(f"[bold blue]ℹ️  Info:[/bold blue] {message}")


@click.group()
@click.version_option(version="1.0.0", prog_name="Captions AI Ads Generator")
def cli():
    """Generate AI-powered advertisement videos using the Captions API."""
    print_banner()


@cli.command()
@click.option("--product-file", "-p", default="product.json", help="Path to product.json file")
@click.option("--output-dir", "-o", default="./generated_videos", help="Output directory for videos")
@click.option("--api-key", help="Captions API key (or set CAPTIONS_API_KEY env var)")
@click.option("--filename", "-f", help="Custom filename for the video")
def generate(product_file: str, output_dir: str, api_key: Optional[str], filename: Optional[str]):
    """Generate an AI advertisement video from product.json."""
    
    try:
        # Load and validate product.json
        if not os.path.exists(product_file):
            print_error(f"Product file not found: {product_file}")
            sys.exit(1)
        
        with open(product_file, 'r') as f:
            try:
                product_data = json.load(f)
            except json.JSONDecodeError as e:
                print_error(f"Invalid JSON in {product_file}: {str(e)}")
                sys.exit(1)
        
        # Validate required fields
        required_fields = ["script", "creatorName", "mediaUrls", "webhookId", "resolution"]
        missing_fields = []
        
        for field in required_fields:
            if field not in product_data:
                missing_fields.append(field)
            elif field == "webhookId":
                # webhookId can be null/None
                pass
            elif product_data[field] is None:
                missing_fields.append(field)
            elif type(product_data[field]) == str and not product_data[field].strip():
                missing_fields.append(field)
            elif field == "mediaUrls":
                if hasattr(product_data[field], '__iter__') and not isinstance(product_data[field], str):
                    if len(product_data[field]) == 0:
                        missing_fields.append(field)
                else:
                    missing_fields.append(field)
        
        if missing_fields:
            print_error(f"Missing or invalid required fields in {product_file}: {', '.join(missing_fields)}")
            print_info("Required fields: script, creatorName, mediaUrls (non-empty array), webhookId, resolution")
            sys.exit(1)
        
        # Validate script length
        if len(product_data["script"].strip()) < 10:
            print_error("Script must be at least 10 characters long.")
            sys.exit(1)
        
        # Validate resolution
        valid_resolutions = ["fhd", "hd", "4k"]
        if product_data["resolution"] not in valid_resolutions:
            print_error(f"Invalid resolution. Must be one of: {', '.join(valid_resolutions)}")
            sys.exit(1)
        
        # Validate media URLs
        for i, url in enumerate(product_data["mediaUrls"]):
            if not validate_url(url):
                print_error(f"Invalid media URL at index {i}: {url}")
                sys.exit(1)
        
        print_info(f"✅ Product configuration loaded from {product_file}")
        print_info(f"📝 Script length: {len(product_data['script'])} characters")
        print_info(f"🎭 Creator: {product_data['creatorName']}")
        print_info(f"🖼️  Media URLs: {len(product_data['mediaUrls'])} images")
        print_info(f"📐 Resolution: {product_data['resolution']}")
        
        # Initialize video generator
        generator = VideoGenerator(api_key)
        
        # Simple status display with timer
        print_info("🎬 Starting AI video generation...")
        
        # Generate the video
        video_path = generator.generate_ad_video(
            script=product_data["script"],
            creator_name=product_data["creatorName"],
            media_urls=product_data["mediaUrls"],
            resolution=product_data["resolution"],
            webhook_id=product_data["webhookId"],
            output_dir=output_dir,
            filename=filename
        )
        
        print_success("✅ Video generation completed!")
        
        # Get file size
        file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
        
        # Display success information
        success_table = Table(title="Video Generation Complete!", show_header=False)
        success_table.add_row("Video Path", video_path)
        success_table.add_row("Creator", product_data["creatorName"])
        success_table.add_row("Resolution", product_data["resolution"].upper())
        success_table.add_row("File Size", format_file_size(file_size))
        
        console.print(success_table)
        print_success(f"Video saved to: {video_path}")
        
    except CaptionsAPIError as e:
        print_error(str(e))
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")
        sys.exit(1)


@cli.command()
@click.option("--api-key", help="Captions API key (or set CAPTIONS_API_KEY env var)")
def creators(api_key: Optional[str]):
    """List available AI creators for ad generation."""
    
    try:
        generator = VideoGenerator(api_key)
        creators_info = generator.list_creators()
        
        # Create creators table
        creators_table = Table(title="Available AI Creators")
        creators_table.add_column("Creator Name", style="cyan")
        creators_table.add_column("Description", style="green")
        
        supported_creators = creators_info.get("supportedCreators", [])
        thumbnails = creators_info.get("thumbnails", {})
        
        if supported_creators:
            for creator in supported_creators:
                description = thumbnails.get(creator, "No description available")
                # Convert description to string if it's a dict
                if isinstance(description, dict):
                    description = str(description)
                creators_table.add_row(creator, description)
        else:
            creators_table.add_row("No creators available", "Please check your API key and try again")
        
        console.print(creators_table)
        
        if supported_creators:
            console.print(f"\n[bold]Total available creators: {len(supported_creators)}[/bold]")
            console.print("\n[bold]Usage Example:[/bold]")
            console.print(f"python main.py generate --script 'Your ad script here' --creator '{supported_creators[0]}'")
        
    except CaptionsAPIError as e:
        print_error(str(e))
        sys.exit(1)


@cli.command()
@click.option("--output-dir", "-o", default="./generated_videos", help="Directory to list videos from")
def list(output_dir: str):
    """List all generated videos in the output directory."""
    
    if not os.path.exists(output_dir):
        print_error(f"Output directory does not exist: {output_dir}")
        sys.exit(1)
    
    video_files = list_generated_videos(output_dir)
    
    if not video_files:
        print_info(f"No video files found in {output_dir}")
        return
    
    # Create videos table
    videos_table = Table(title=f"Generated Videos in {output_dir}")
    videos_table.add_column("Filename", style="cyan")
    videos_table.add_column("Size", style="yellow")
    videos_table.add_column("Modified", style="green")
    
    for video_path in video_files:
        filename = os.path.basename(video_path)
        size_mb = os.path.getsize(video_path) / (1024 * 1024)
        modified_time = os.path.getmtime(video_path)
        
        from datetime import datetime
        modified_str = datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d %H:%M")
        
        videos_table.add_row(
            filename,
            format_file_size(size_mb),
            modified_str
        )
    
    console.print(videos_table)


@cli.command()
@click.option("--script", "-s", required=True, help="Script to validate")
@click.option("--creator", "-c", required=True, help="Creator name to validate")
def validate(script: str, creator: str):
    """Validate a script and creator combination."""
    
    # Validate script
    if len(script.strip()) < 10:
        print_error("Script must be at least 10 characters long.")
        return
    
    print_success("Script is valid!")
    print_info(f"Script length: {len(script)} characters")
    print_info(f"Creator: {creator}")
    
    # Show usage example
    console.print("\n[bold]Usage Example:[/bold]")
    console.print(f"python main.py generate --script '{script[:50]}...' --creator '{creator}'")


@cli.command()
def setup():
    """Interactive setup for API configuration."""
    
    console.print("[bold]Captions AI Ads Generator Setup[/bold]\n")
    
    # Check if .env file exists
    env_file = Path(".env")
    if env_file.exists():
        console.print("✅ .env file already exists")
    else:
        console.print("📝 Creating .env file...")
        
        # Get API key from user
        api_key = click.prompt("Enter your Captions API key", type=str)
        
        # Write to .env file
        env_content = f"""# Captions API Configuration
CAPTIONS_API_KEY={api_key}

# Optional: Default settings
DEFAULT_VIDEO_DURATION=30
DEFAULT_VIDEO_STYLE=professional
DEFAULT_OUTPUT_DIR=./generated_videos
"""
        
        with open(".env", "w") as f:
            f.write(env_content)
        
        print_success("Configuration saved to .env file")
    
    # Test API connection
    console.print("\n🔍 Testing API connection...")
    try:
        generator = VideoGenerator()
        credits_info = generator.get_credits_info()
        balance = credits_info.get("balance", 0)
        print_success(f"API connection successful! Available credits: {balance}")
    except CaptionsAPIError as e:
        print_error(f"API connection failed: {str(e)}")
        console.print("\n[bold]Troubleshooting:[/bold]")
        console.print("1. Make sure your API key is correct")
        console.print("2. Ensure you have credits in your account")
        console.print("3. Check your internet connection")
    except Exception as e:
        print_error(f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    cli() 