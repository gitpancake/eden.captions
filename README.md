# Captions AI Ads Generator

A Python application that generates promotional videos using the Captions AI Ads API. Simply provide a product URL and get a professionally generated advertisement video.

## Features

- 🎬 Generate AI-powered advertisement videos from product URLs
- 💾 Automatic video download and saving
- 📊 Real-time progress tracking
- 🔧 Configurable video settings
- 🎨 Beautiful CLI interface with rich formatting

## Prerequisites

- Python 3.8 or higher
- Captions API account with credits
- API key from the [Captions API Dashboard](https://help.captions.ai/api-reference/api)

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd eden.captions
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your environment variables:

```bash
cp .env.example .env
```

4. Edit `.env` file with your API key:

```
CAPTIONS_API_KEY=your_api_key_here
```

## Usage

### Basic Usage

Generate a video from a product.json file:

```bash
python main.py generate
```

### Advanced Usage

Generate a video with custom settings:

```bash
python main.py generate \
  --product-file "my_product.json" \
  --output-dir "./videos"
```

### Product Configuration

Create a `product.json` file with the following structure:

```json
{
  "script": "Your advertisement script here",
  "creatorName": "Jason",
  "mediaUrls": ["https://example.com/image1.jpg", "https://example.com/image2.jpg"],
  "webhookId": "your_webhook_id",
  "resolution": "fhd"
}
```

**Required Fields:**

- `script`: Advertisement script (minimum 10 characters)
- `creatorName`: Name of the AI creator to use
- `mediaUrls`: Array of image URLs (at least one required)
- `webhookId`: Webhook identifier for notifications
- `resolution`: Video resolution ("fhd", "hd", or "4k")

### Available Options

- `--product-file`: Path to product.json file (default: "product.json")
- `--output-dir`: Directory to save videos (default: "./generated_videos")
- `--api-key`: API key (can also use environment variable)
- `--filename`: Custom filename for the video

## API Pricing

- 1 credit per second of video generated
- Rate limit: 5 requests per minute
- Each credit costs $0.05

## Project Structure

```
eden.captions/
├── main.py                 # Main CLI application
├── captions_api.py         # Captions API client
├── video_generator.py      # Video generation logic
├── utils.py               # Utility functions
├── product.json           # Product configuration file
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Error Handling

The application handles various error scenarios:

- Invalid API keys
- Missing or invalid product.json fields
- Invalid media URLs
- Rate limiting
- Network errors
- Invalid JSON format

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
