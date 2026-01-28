# Vision MCP Server

Free, unlimited vision capabilities for your AI coding assistant using Groq API and Meta Llama 4 Vision model.

## Features

- **Image Analysis** - Understand and describe images
- **Text Extraction (OCR)** - Extract text from screenshots, documents, photos
- **UI Analysis** - Describe UI components, layouts, and design
- **Error Diagnosis** - Analyze error screenshots and suggest fixes
- **Diagram Understanding** - Interpret flowcharts, UML, architecture diagrams
- **Chart Analysis** - Read charts and dashboards for insights
- **Image Comparison** - Compare two images for differences
- **Code Extraction** - Extract code from IDE screenshots

## Installation

### Prerequisites

- Python 3.10 or higher
- Free Groq API key

### Get Groq API Key (Free)

1. Visit https://console.groq.com/keys
2. Sign up (free)
3. Create a new API key

### Install Dependencies

```bash
cd vision-mcp-server

# Option 1: Using install script (recommended)
./install.sh

# Option 2: Manual installation
pip3 install mcp groq pillow aiofiles
```

## Configuration

### Claude Desktop

Add to `~/.claude/config.json`:

```json
{
  "mcpServers": {
    "vision-mcp-server": {
      "command": "python",
      "args": ["-m", "vision_mcp_server.server"],
      "env": {
        "GROQ_API_KEY": "your-groq-api-key-here"
      }
    }
  }
}
```

### OpenCode

Add to OpenCode settings:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "vision-mcp-server": {
      "type": "local",
      "command": ["python", "-m", "vision_mcp_server.server"],
      "environment": {
        "GROQ_API_KEY": "your-groq-api-key-here"
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
      "command": "python",
      "args": ["-m", "vision_mcp_server.server"],
      "env": {
        "GROQ_API_KEY": "your-groq-api-key-here"
      }
    }
  }
}
```

## Usage

### Analyze Image
```
Describe this image: screenshot.png
```

### Extract Text
```
Extract text from this document: scan.jpg
```

### Diagnose Error
```
What's wrong with this error screenshot: error.png
```

### Understand Diagram
```
Explain this architecture diagram: system-diagram.png
```

### Compare Images
```
Compare these two UI screenshots: old-ui.png vs new-ui.png
```

## Available Tools

- `analyze_image` - General image analysis
- `extract_text` - OCR text extraction
- `describe_ui` - UI component analysis
- `diagnose_error` - Error screenshot analysis
- `understand_diagram` - Diagram interpretation
- `analyze_chart` - Chart and dashboard analysis
- `compare_images` - Image comparison
- `code_from_screenshot` - Code extraction from screenshots

## Models Used

- **meta-llama/llama-4-scout-17b-16e-instruct** - Latest Meta Llama 4 vision model
- Available for free via Groq API
- No quotas, no limits
- Superior vision capabilities and multimodal performance

## Testing

Run locally:

```bash
export GROQ_API_KEY=your-api-key
python -m vision_mcp_server.server
```

## License

MIT
