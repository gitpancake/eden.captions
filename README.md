# Captions AI Ads Generator

A Python application that generates professional AI-powered advertisement videos using the Captions AI Ads API. Simply provide a script and media URLs to create engaging promotional content.

## Features

- 🎬 Generate AI-powered advertisement videos from scripts and media
- 🎭 Multiple AI creators to choose from (Jason, Sarah, etc.)
- 💾 Automatic video download and organization
- 📊 Real-time progress tracking with beautiful CLI interface
- 🔧 Configurable video settings (resolution, creator, etc.)
- 🎨 Rich formatting and status updates
- 📝 Script validation and optimization

## Prerequisites

- Python 3.8 or higher
- Captions API account with credits
- API key from [Captions AI](https://captions.ai)

## Installation

1. **Clone or download** the project files to your local machine

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API key:**

   ```bash
   python main.py setup
   ```

   Or manually create a `.env` file:

   ```bash
   echo "CAPTIONS_API_KEY=your_api_key_here" > .env
   ```

## Quick Start

1. **Generate your first video:**

   ```bash
   python main.py generate
   ```

   This uses the default `product.json` configuration.

2. **View available AI creators:**

   ```bash
   python main.py creators
   ```

3. **List generated videos:**
   ```bash
   python main.py list
   ```

## Usage

### Basic Video Generation

Generate a video using the default `product.json`:

```bash
python main.py generate
```

### Custom Configuration

Generate a video with custom settings:

```bash
python main.py generate \
  --product-file "my_product.json" \
  --output-dir "./custom_videos" \
  --filename "my_custom_video"
```

### Product Configuration

Create a `product.json` file with your video specifications:

```json
{
  "script": "Transform your Toyota 4Runner with our premium liftgate supports! These heavy-duty gas struts provide effortless lifting and secure holding, making loading and unloading a breeze. Perfect for outdoor enthusiasts, contractors, and anyone who needs reliable access to their cargo area. Easy installation, durable construction, and backed by our satisfaction guarantee. Don't struggle with a heavy liftgate - upgrade to professional-grade supports today!",
  "creatorName": "Jason",
  "mediaUrls": ["https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&h=600&fit=crop", "https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=800&h=600&fit=crop"],
  "webhookId": null,
  "resolution": "fhd"
}
```

**Required Fields:**

- `script`: Your advertisement script (minimum 10 characters)
- `creatorName`: AI creator name (use `python main.py creators` to see available options)
- `mediaUrls`: Array of image URLs (at least one required)
- `webhookId`: Webhook identifier (can be null)
- `resolution`: Video resolution ("fhd", "hd", or "4k")

### Available Commands

| Command    | Description                               |
| ---------- | ----------------------------------------- |
| `generate` | Generate a video from product.json        |
| `creators` | List available AI creators                |
| `list`     | List all generated videos                 |
| `validate` | Validate a script and creator combination |
| `setup`    | Interactive API setup                     |

### Command Options

**Generate Command:**

- `--product-file, -p`: Path to product.json file (default: "product.json")
- `--output-dir, -o`: Directory to save videos (default: "./generated_videos")
- `--api-key`: API key (can also use environment variable)
- `--filename, -f`: Custom filename for the video

**Examples:**

```bash
# Generate with custom product file
python main.py generate --product-file "my_product.json"

# Generate with custom output directory
python main.py generate --output-dir "./videos"

# Generate with custom filename
python main.py generate --filename "my_video"

# Validate script before generating
python main.py validate --script "Your script here" --creator "Jason"
```

## Video Generation Process

1. **Script Validation**: Ensures your script meets minimum requirements
2. **API Submission**: Sends your request to Captions AI
3. **Progress Tracking**: Real-time updates on video generation status
4. **Download**: Automatically downloads the completed video
5. **Organization**: Saves videos with descriptive filenames

## Output

Videos are saved to `./generated_videos/` with the format:

```
ai_ad_[Creator]_[Resolution]_[Timestamp].mp4
```

Example: `ai_ad_Jason_fhd_20250803_144946.mp4`

## API Pricing & Limits

- **Credits**: 1 credit per second of video generated
- **Cost**: Approximately $0.05 per credit
- **Rate Limit**: 5 requests per minute
- **Resolutions**: fhd (Full HD), hd (HD), 4k (4K)

## Project Structure

```
eden.captions/
├── main.py                    # Main CLI application
├── captions_api.py           # Captions API client
├── video_generator.py        # Video generation logic
├── utils.py                  # Utility functions
├── product.json              # Product configuration file
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── generated_videos/         # Generated video files
└── README.md                # This file
```

## Troubleshooting

### Common Issues

1. **API Key Issues**

   ```bash
   # Test your API connection
   python main.py setup
   ```

2. **Invalid Product Configuration**

   ```bash
   # Check required fields in product.json
   python main.py generate
   ```

3. **Script Too Short**

   - Ensure your script is at least 10 characters long

4. **Invalid Media URLs**

   - Verify your image URLs are accessible
   - Use HTTPS URLs for best compatibility

5. **Rate Limiting**
   - Wait 1 minute between requests
   - Check your API credits balance

### Error Messages

- `Invalid API key`: Check your CAPTIONS_API_KEY environment variable
- `Missing required fields`: Ensure all required fields are in product.json
- `Script must be at least 10 characters`: Make your script longer
- `Invalid media URL`: Check your image URLs are valid and accessible
- `Rate limit exceeded`: Wait before making another request

## Examples

### Example 1: Product Launch Video

```json
{
  "script": "Introducing our revolutionary new product! Transform your daily routine with cutting-edge technology that makes life easier. Perfect for busy professionals who demand the best. Easy to use, powerful results, and backed by our satisfaction guarantee. Don't miss out - upgrade today!",
  "creatorName": "Sarah",
  "mediaUrls": ["https://images.unsplash.com/photo-1234567890?w=800&h=600&fit=crop"],
  "webhookId": null,
  "resolution": "fhd"
}
```

### Example 2: Service Promotion

```json
{
  "script": "Looking for reliable automotive solutions? Our professional team delivers exceptional service with every visit. From routine maintenance to complex repairs, we've got you covered. Trusted by thousands of satisfied customers. Book your appointment today and experience the difference!",
  "creatorName": "Jason",
  "mediaUrls": ["https://images.unsplash.com/photo-0987654321?w=800&h=600&fit=crop", "https://images.unsplash.com/photo-1122334455?w=800&h=600&fit=crop"],
  "webhookId": null,
  "resolution": "hd"
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is part of the Eden Captions AI integration suite.
