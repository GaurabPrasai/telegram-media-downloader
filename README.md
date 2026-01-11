# Telegram Media Downloader

A Python script that efficiently downloads all media files from Telegram channels with parallel download support.

## Features

- **Parallel Downloads**: Download multiple files simultaneously for faster operation
- **Smart File Naming**: Automatically generates safe, Windows-compatible filenames with date prefixes
- **Resume Support**: Skips already downloaded files automatically
- **Comprehensive Media Support**: Downloads videos, images, audio, documents, and other file attachments
- **Error Handling**: Robust error handling with detailed reporting
- **Progress Tracking**: Real-time download progress and statistics

## What Gets Downloaded

✅ **Supported Media Types:**
- Videos
- Images
- Audio files
- Documents (PDFs, ZIPs, etc.)
- Any file attachments that Telegram considers "media"
- Voice messages

❌ **Not Downloaded:**
- Plain text messages
- URLs/links in messages
- Message content

## Prerequisites

- Python 3.7 or higher
- A Telegram account
- Telegram API credentials (API ID and API Hash)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/telegram-media-downloader.git
cd telegram-media-downloader
```

2. Install required dependencies:
```bash
pip install telethon
```

## Getting Your Telegram API Credentials

1. Visit [https://my.telegram.org](https://my.telegram.org)
2. Log in with your Telegram account
3. Go to "API development tools"
4. Create a new application (if you haven't already)
5. Copy your `API_ID` and `API_HASH`

## Configuration

Open `telegram_downloader.py` and configure the following variables:

```python
DOWNLOAD_FOLDER = r"C:\Telegram download"  # Where files will be saved
CHANNEL = "https://telegram.me/channel-url"  # Target channel link or @username
LIMIT = 5  # Number of messages to scan
API_ID = 0  # Your API ID from my.telegram.org
API_HASH = ""  # Your API Hash from my.telegram.org
SESSION_NAME = "mySession"  # Session file name
MAX_PARALLEL = 5  # Number of concurrent downloads
```

### Channel Format

- **Public channels**: Use `@channelname` or full URL
- **Private channels**: Use the invite link or hash

## Usage

Run the script:

```bash
python telegram_downloader.py
```

On first run, you'll be prompted to enter your phone number and verification code to authenticate with Telegram.

## Configuration Options

| Variable | Description | Default |
|----------|-------------|---------|
| `DOWNLOAD_FOLDER` | Destination folder for downloads | `C:\Telegram download` |
| `CHANNEL` | Target Telegram channel | Required |
| `LIMIT` | Number of recent messages to scan | `5` |
| `API_ID` | Your Telegram API ID | Required |
| `API_HASH` | Your Telegram API Hash | Required |
| `SESSION_NAME` | Name for session file | `mySession` |
| `MAX_PARALLEL` | Concurrent downloads | `5` |


## Troubleshooting

**"Cannot access channel" error:**
- Verify you have access to the channel
- For public channels, use `@channelname` format
- For private channels, make sure you've joined the channel first

**Authentication errors:**
- Ensure your API_ID and API_HASH are correct
- Delete the session file and try again

**No media found:**
- Increase the `LIMIT` value to scan more messages
- Verify the channel contains media files

## Legal Notice

This tool uses the official Telegram API and is intended for personal use only. Users are responsible for:

- Complying with Telegram's Terms of Service
- Respecting copyright and intellectual property rights
- Obtaining necessary permissions before downloading content
- Using downloaded content in accordance with applicable laws

## License

MIT License - See LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is provided as-is without any warranties. The developers are not responsible for any misuse or legal consequences arising from the use of this software.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.
