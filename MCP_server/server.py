# Day 10 - 12 | Phase 2.3, 2.4 and 2.5

import os
import sys
from mcp.server.fastmcp import FastMCP
from monolith_agent.coordinator import Coordinator

coordinator = Coordinator()

# ------------------------------------------------------------------------------

API_KEY = os.environ.get("MY_API_KEY", "")
PORT = os.environ.get("CONTENT_SERVER_PORT", "8000")
INSTANCE = os.environ.get("SERVER_INSTANCE", "project")

def log(message: str) -> None:
    """Log messages to STDERR only."""
    print(
        f"[ContentServer:{INSTANCE}] {message}",
        file=sys.stderr,
        flush=True
    )

log(
    f"starting | instance={INSTANCE} port={PORT} "
    f"api_key={'SET' if API_KEY else 'MISSING'}"
)

# Create MCP Server
mcp = FastMCP("ContentServer")

# ------------------------------------------------------------------------------
# Tool 1 - extract_data
# ------------------------------------------------------------------------------
#

@mcp.tool()
def extract_data(text: str):
    """
    Extract names, email addresses,
    phone numbers and other important
    structured information from text.
    """

    if not text.strip():
        return {
            "isError": True,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": "Text cannot be empty"
        }

    if text == "no_results":
        return {
            "isError": False,
            "results": []
        }

    return {
        "isError": False,
        "results": {
            "names": ["Harini"],
            "emails": ["harini@gmail.com"]
        }
    }

# ------------------------------------------------------------------------------
# Tool 2 - analyze_content
# ------------------------------------------------------------------------------

@mcp.tool()
def analyze_content(text: str):
    # """
    # Analyze a piece of text and return insights about it.
    # Use this whenever the user wants text analyzed.
    # """
    """
        Analyze general text such as emails,
    articles, notes, and blog posts.
    """

    if not text.strip():
        return {
            "isError": True,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": "Text cannot be empty"
        }

    if text == "server_down":
        return {
            "isError": True,
            "errorCategory": "transient",
            "isRetryable": True,
            "message": "Temporary service unavailable"
        }

    return {
        "isError": False,
        "results": {
            "analysis": "Content analysis completed"
        }
    }

# ------------------------------------------------------------------------------
# Tool 3 - analyze_document
# ------------------------------------------------------------------------------

@mcp.tool()
def analyze_document(text: str):
    # """
    # Analyze a document or text and return insights about it.
    # Use this whenever the user wants a document analyzed.
    # """
    """
    Analyze reports, resumes,
    invoices and PDFs.

    Use for formal documents.
    """

    if not text.strip():
        return {
            "isError": True,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": "Document cannot be empty"
        }

    if text == "invalid_document":
        return {
            "isError": True,
            "errorCategory": "business",
            "isRetryable": False,
            "message": "Document cannot be processed"
        }

    return {
        "isError": False,
        "results": {
            "analysis": "Document analysis completed"
        }
    }

# ------------------------------------------------------------------------------
# Tool 4 - summarize
# ------------------------------------------------------------------------------

@mcp.tool()
def summarize(text: str):
    """Generate a concise summary while preserving important information."""

    if not text.strip():
        return {
            "isError": True,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": "Text cannot be empty"
        }

    return {
        "isError": False,
        "results": {
            "summary": "This is a summary"
        }
    }

# ------------------------------------------------------------------------------
# Tool 5 - verify
# ------------------------------------------------------------------------------

@mcp.tool()
def verify(claim: str):
    """Verify whether a factual claim appears to be correct."""

    if not claim.strip():
        return {
            "isError": True,
            "errorCategory": "validation",
            "isRetryable": False,
            "message": "Claim cannot be empty"
        }

    if claim == "restricted":
        return {
            "isError": True,
            "errorCategory": "permission",
            "isRetryable": False,
            "message": "Access denied"
        }

    return {
        "isError": False,
        "results": {
            "verified": True
        }
    }

# CONNECTING  COORDINATOR TO MCP

@mcp.tool()
def coordinator_router(request: str):
    """
    Route requests through specialized agents.
    """
    return coordinator.handle_request(request)
# ------------------------------------------------------------------------------
# MCP Resource Catalog (Phase 2.5)
# ------------------------------------------------------------------------------

@mcp.resource("catalog://topics")
def catalog():
    return """
    Content Server Catalog

    Topics covered:
    - Text extraction
    - Content analysis
    - Document analysis
    - Summarization
    - Claim verification
    - Multi-agent request routing

    Available tools:
    - extract_data
    - analyze_content
    - analyze_document
    - summarize
    - verify
    - coordinator_router
    """

# ------------------------------------------------------------------------------
# Run Server
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()