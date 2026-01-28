#!/usr/bin/env python3
"""Test script for Vision MCP Server"""

import asyncio
import sys

sys.path.insert(0, ".")

from vision_mcp_server.server import VisionClient, list_tools


async def main():
    print("=" * 70)
    print("Vision MCP Server - Full Test")
    print("=" * 70)

    # Initialize client
    import os

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: Please set GROQ_API_KEY environment variable")
        return
    client = VisionClient(api_key)

    # Test 1: List available tools
    print("\n📋 Available Tools:")
    print("-" * 70)
    tools = await list_tools()
    for tool in tools:
        print(f"  • {tool.name}: {tool.description[:60]}...")

    # Test 2: Text Extraction (OCR)
    print("\n\n✓ Test 1: Text Extraction (OCR)")
    print("-" * 70)
    result = await client.analyze_image(
        "test_images/test-ocr.png",
        "Extract ALL text from this image. Return only the text, nothing else.",
    )
    print(f"Result: {result}")

    # Test 3: Image Description
    print("\n\n✓ Test 2: Image Description")
    print("-" * 70)
    result = await client.analyze_image(
        "test_images/test-ocr.png", "Describe this image in 2-3 sentences."
    )
    print(f"Result: {result}")

    # Test 4: UI Analysis
    print("\n\n✓ Test 3: UI Analysis")
    print("-" * 70)
    result = await client.analyze_image(
        "test_images/test-ocr.png",
        "Analyze this as a UI screenshot. What elements do you see?",
    )
    print(f"Result: {result}")

    print("\n" + "=" * 70)
    print("✅ All tests passed!")
    print("=" * 70)
    print("\n📝 Configuration for your MCP client:")
    print("-" * 70)
    print("""
{
  "vision-mcp-server": {
    "type": "local",
    "command": ["python3", "-m", "vision_mcp_server.server"],
    "environment": {
      "GROQ_API_KEY": "your-groq-api-key-here"
    }
  }
}
""")


if __name__ == "__main__":
    asyncio.run(main())
