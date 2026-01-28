# Quick Start Guide

## Prerequisites

- Python 3.10 or higher
- Free Groq API key

## Step 1: Install Dependencies

```bash
cd vision-mcp-server

# Option 1: Using install script
./install.sh

# Option 2: Manual installation
pip3 install mcp groq pillow aiofiles
```

## Step 2: Get Groq API Key

1. Visit https://console.groq.com/keys
2. Sign up for free account
3. Create new API key
4. Copy the key

## Step 3: Configure Your Client

### OpenCode

Add to your OpenCode configuration file:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "vision-mcp-server": {
      "type": "local",
      "command": ["python3", "-m", "vision_mcp_server.server"],
      "environment": {
        "GROQ_API_KEY": "gsk_your-actual-api-key-here"
      }
    }
  }
}
```

### Claude Desktop

Add to `~/.claude/config.json`:

```json
{
  "mcpServers": {
    "vision-mcp-server": {
      "command": "python3",
      "args": ["-m", "vision_mcp_server.server"],
      "env": {
        "GROQ_API_KEY": "gsk_your-actual-api-key-here"
      }
    }
  }
}
```

### Cline (VS Code)

Add to Cline settings:

```json
{
  "mcpServers": {
    "vision-mcp-server": {
      "command": "python3",
      "args": ["-m", "vision_mcp_server.server"],
      "env": {
        "GROQ_API_KEY": "gsk_your-actual-api-key-here"
      }
    }
  }
}
```

## Step 4: Test the Server

```bash
# Set your API key
export GROQ_API_KEY=gsk_your-actual-api-key-here

# Run the server (for testing)
python3 -m vision_mcp_server.server
```

## Usage Examples

### Analyze an Image
```
What's in this screenshot.png?
Describe the image: photo.jpg
```

### Extract Text
```
Extract all text from this document: scan.jpg
What text is visible in screenshot.png?
```

### Diagnose Error
```
What's wrong with this error: error-screenshot.png
Help me fix this error
```

### Understand Diagram
```
Explain this diagram: architecture.png
What does this flowchart show?
```

### Compare Images
```
Compare old-ui.png and new-ui.png
What's the difference between screenshot1.jpg and screenshot2.jpg?
```

### Analyze Chart
```
What insights can you get from this dashboard.png?
Analyze the chart: graph.jpg
```

### Extract Code
```
Extract the code from this IDE screenshot: code.png
What's the code in this image?
```

## Troubleshooting

### Module not found error
```bash
pip3 install --user mcp groq pillow aiofiles
```

### API Key error
- Make sure GROQ_API_KEY is set correctly
- Get a new key from https://console.groq.com/keys

### Permission denied
```bash
chmod +x install.sh
```

### Python not found
- Install Python 3.10+: https://www.python.org/downloads/

## Project Structure

```
vision-mcp-server/
├── vision_mcp_server/
│   ├── __init__.py
│   └── server.py          # Main MCP server implementation
├── pyproject.toml         # Package configuration
├── README.md              # Documentation
├── QUICKSTART.md          # This file
└── install.sh             # Installation script
```

## Features

All tools are free and unlimited:

- ✅ Image Analysis
- ✅ Text Extraction (OCR)
- ✅ UI Description
- ✅ Error Diagnosis
- ✅ Diagram Understanding
- ✅ Chart Analysis
- ✅ Image Comparison
- ✅ Code Extraction

## Support

For issues:
1. Check Groq API status: https://status.groq.com/
2. Verify your API key
3. Check error messages

## License

MIT - Free to use and modify
