#!/usr/bin/env python3
"""
Example usage of the Captions AI Ads Generator

This script demonstrates how to use the video generator programmatically.
"""

import os
from dotenv import load_dotenv
from video_generator import VideoGenerator
from captions_api import CaptionsAPIError

# Load environment variables
load_dotenv()


def main():
    """Example usage of the video generator."""
    
    # Example product URLs
    example_urls = [
        "https://www.apple.com/iphone-15/",
        "https://www.nike.com/t/air-max-270-shoe-KkLcGR",
        "https://www.amazon.com/dp/B08N5WRWNW"  # Example product
    ]
    
    try:
        # Initialize the video generator
        generator = VideoGenerator()
        
        # Check credits first
        print("🔍 Checking credits...")
        credits_info = generator.get_credits_info()
        balance = credits_info.get("balance", 0)
        print(f"Available credits: {balance}")
        
        if balance < 30:
            print("⚠️  Insufficient credits for a 30-second video. Need at least 30 credits.")
            return
        
        # Generate a video for the first example URL
        product_url = example_urls[0]
        print(f"\n🎬 Generating AI ad for: {product_url}")
        
        video_path = generator.generate_ad_video(
            product_url=product_url,
            duration=30,
            style="professional",
            output_dir="./example_videos"
        )
        
        print(f"✅ Video generated successfully!")
        print(f"📁 Saved to: {video_path}")
        
        # Get file size
        file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
        print(f"📊 File size: {file_size:.1f} MB")
        
    except CaptionsAPIError as e:
        print(f"❌ API Error: {str(e)}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")


def batch_generate_example():
    """Example of generating multiple videos in batch."""
    
    example_urls = [
        "https://www.apple.com/iphone-15/",
        "https://www.nike.com/t/air-max-270-shoe-KkLcGR"
    ]
    
    styles = ["professional", "energetic"]
    
    try:
        generator = VideoGenerator()
        
        for i, url in enumerate(example_urls):
            style = styles[i % len(styles)]
            print(f"\n🎬 Generating {style} ad for: {url}")
            
            video_path = generator.generate_ad_video(
                product_url=url,
                duration=15,  # Shorter duration for batch processing
                style=style,
                output_dir="./batch_videos"
            )
            
            print(f"✅ Generated: {video_path}")
            
    except CaptionsAPIError as e:
        print(f"❌ API Error: {str(e)}")


if __name__ == "__main__":
    print("🎬 Captions AI Ads Generator - Example Usage\n")
    
    # Run single video generation example
    main()
    
    # Uncomment to run batch generation example
    # print("\n" + "="*50)
    # print("Batch Generation Example")
    # print("="*50)
    # batch_generate_example() 