#!/bin/bash
# Installation script for Vision MCP Server

echo "Installing Vision MCP Server..."

# Check Python version
python3 --version || { echo "Python 3.10+ is required"; exit 1; }

# Install pip if not available
if ! command -v pip3 &> /dev/null; then
    echo "pip3 not found. Installing..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py --user
    export PATH="$HOME/.local/bin:$PATH"
    rm get-pip.py
fi

# Install package
pip3 install -e .

echo ""
echo "Installation complete!"
echo ""
echo "Next steps:"
echo "1. Get your free Groq API key from: https://console.groq.com/keys"
echo "2. Set GROQ_API_KEY environment variable"
echo "3. Add server configuration to your MCP client (see README.md)"
echo ""
echo "Test the server:"
echo "export GROQ_API_KEY=your-key-here"
echo "python3 -m vision_mcp_server.server"
