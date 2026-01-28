import asyncio
import base64
import mimetypes
from pathlib import Path
from typing import Any

from groq import Groq, AsyncGroq
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    ImageContent,
    TextContent,
)

SERVER_NAME = "vision-mcp-server"
SERVER_VERSION = "0.1.0"

server = Server(SERVER_NAME)

VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


class VisionClient:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        self.async_client = AsyncGroq(api_key=api_key)

    async def analyze_image(
        self, image_path: str, prompt: str, model: str = VISION_MODEL
    ) -> str:
        """Analyze image using vision model"""
        image_base64 = await self._encode_image(image_path)

        response = await self.async_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_base64}"
                            },
                        },
                    ],
                }
            ],
            temperature=0.7,
            max_tokens=2048,
        )

        return response.choices[0].message.content

    async def compare_images(
        self, image1_path: str, image2_path: str, comparison_type: str = "general"
    ) -> str:
        """Compare two images"""
        image1_base64 = await self._encode_image(image1_path)
        image2_base64 = await self._encode_image(image2_path)

        prompt = f"""Compare these two images. Focus on: {comparison_type}
        Provide a detailed comparison highlighting similarities and differences."""

        response = await self.async_client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image1_base64}"
                            },
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image2_base64}"
                            },
                        },
                    ],
                }
            ],
            temperature=0.5,
            max_tokens=2048,
        )

        return response.choices[0].message.content

    async def _encode_image(self, image_path: str) -> str:
        """Encode image to base64"""
        async with aiofiles.open(image_path, "rb") as f:
            image_data = await f.read()
        return base64.b64encode(image_data).decode("utf-8")


vision_client = None


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available vision tools"""
    return [
        Tool(
            name="analyze_image",
            description="Analyze an image with AI. Provide detailed description, understanding of content, and answer questions about the image.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the image file",
                    },
                    "prompt": {
                        "type": "string",
                        "description": "Question or instruction for image analysis (default: 'Describe this image in detail')",
                        "default": "Describe this image in detail",
                    },
                },
                "required": ["image_path"],
            },
        ),
        Tool(
            name="extract_text",
            description="Extract and recognize all text from an image using OCR capabilities. Works with screenshots, documents, photos with text.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the image file containing text",
                    }
                },
                "required": ["image_path"],
            },
        ),
        Tool(
            name="describe_ui",
            description="Describe UI elements, layout, and design of a screenshot. Identify buttons, forms, navigation, and interface components.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the UI screenshot",
                    }
                },
                "required": ["image_path"],
            },
        ),
        Tool(
            name="diagnose_error",
            description="Analyze error screenshots and propose actionable fixes. Describe the error message, context, and suggest solutions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the error screenshot",
                    }
                },
                "required": ["image_path"],
            },
        ),
        Tool(
            name="understand_diagram",
            description="Interpret architecture diagrams, flowcharts, UML diagrams, ER diagrams, and system diagrams. Explain components and relationships.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the diagram image",
                    }
                },
                "required": ["image_path"],
            },
        ),
        Tool(
            name="analyze_chart",
            description="Read charts, graphs, and dashboards to surface insights, trends, and data points. Explain what the visualization shows.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the chart or dashboard image",
                    }
                },
                "required": ["image_path"],
            },
        ),
        Tool(
            name="compare_images",
            description="Compare two images to identify similarities, differences, and changes. Useful for UI diffs, version comparisons.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image1_path": {
                        "type": "string",
                        "description": "Path to the first image",
                    },
                    "image2_path": {
                        "type": "string",
                        "description": "Path to the second image",
                    },
                    "comparison_type": {
                        "type": "string",
                        "description": "Type of comparison: general, visual, content, layout",
                        "default": "general",
                    },
                },
                "required": ["image1_path", "image2_path"],
            },
        ),
        Tool(
            name="code_from_screenshot",
            description="Extract code from screenshots, IDE screenshots, or code images. Identify the programming language and provide clean, formatted code.",
            inputSchema={
                "type": "object",
                "properties": {
                    "image_path": {
                        "type": "string",
                        "description": "Path to the code screenshot",
                    }
                },
                "required": ["image_path"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool calls"""
    global vision_client

    if not vision_client:
        return [
            TextContent(
                type="text",
                text="Error: Vision client not initialized. Please set GROQ_API_KEY environment variable.",
            )
        ]

    try:
        if name == "analyze_image":
            image_path = arguments.get("image_path")
            prompt = arguments.get("prompt", "Describe this image in detail")
            result = await vision_client.analyze_image(image_path, prompt)

        elif name == "extract_text":
            image_path = arguments.get("image_path")
            prompt = """Extract ALL text from this image. 
            Return only the extracted text, nothing else. Preserve formatting and structure as much as possible."""
            result = await vision_client.analyze_image(image_path, prompt)

        elif name == "describe_ui":
            image_path = arguments.get("image_path")
            prompt = """Analyze this UI screenshot. Describe:
            1. Overall layout and structure
            2. UI components (buttons, forms, navigation, inputs)
            3. Design patterns and style
            4. Any visible text or labels
            Be detailed and specific."""
            result = await vision_client.analyze_image(image_path, prompt)

        elif name == "diagnose_error":
            image_path = arguments.get("image_path")
            prompt = """Analyze this error screenshot. Provide:
            1. The error message exactly as shown
            2. Context and what may have caused it
            3. Specific actionable steps to fix it
            4. Preventive measures for the future
            Be practical and solution-oriented."""
            result = await vision_client.analyze_image(image_path, prompt)

        elif name == "understand_diagram":
            image_path = arguments.get("image_path")
            prompt = """Analyze this diagram. Provide:
            1. Type of diagram (flowchart, UML, architecture, etc.)
            2. Main components and their roles
            3. Relationships and connections
            4. Flow or logic shown
            5. Key insights and purpose
            Be thorough and explain clearly."""
            result = await vision_client.analyze_image(image_path, prompt)

        elif name == "analyze_chart":
            image_path = arguments.get("image_path")
            prompt = """Analyze this chart or dashboard. Provide:
            1. Type of visualization (bar chart, line chart, etc.)
            2. Data shown and axes/labels
            3. Key trends and patterns
            4. Notable data points or anomalies
            5. Insights and conclusions
            Be analytical and data-focused."""
            result = await vision_client.analyze_image(image_path, prompt)

        elif name == "compare_images":
            image1_path = arguments.get("image1_path")
            image2_path = arguments.get("image2_path")
            comparison_type = arguments.get("comparison_type", "general")
            result = await vision_client.compare_images(
                image1_path, image2_path, comparison_type
            )

        elif name == "code_from_screenshot":
            image_path = arguments.get("image_path")
            prompt = """Extract all code from this screenshot. Provide:
            1. Programming language used
            2. Complete, clean code with proper formatting
            3. Preserve indentation and structure
            4. Include comments if visible
            Return the code in markdown code blocks with language specified."""
            result = await vision_client.analyze_image(image_path, prompt)

        else:
            result = f"Unknown tool: {name}"

        return [TextContent(type="text", text=result)]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


import aiofiles


async def main():
    """Main entry point"""
    import os

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY environment variable is required")
        print("Get your free API key from: https://console.groq.com/keys")
        return

    global vision_client
    vision_client = VisionClient(api_key)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
