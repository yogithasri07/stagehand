
import requests
from mcp.server.fastmcp import FastMCP

from state_manager import (
    list_looks,
    get_look,
    set_current_look,
    recall_last_look,
    set_intensity,
    get_status,
)

# Create the Stagehand MCP server
mcp = FastMCP("Stagehand")

TOUCHDESIGNER_URL = "http://127.0.0.1:9980"


def send_to_touchdesigner(endpoint: str, payload: dict) -> dict:
    """Send a request to TouchDesigner and return its response."""
    try:
        response = requests.post(
            f"{TOUCHDESIGNER_URL}/{endpoint}",
            json=payload,
            timeout=5,
        )
        response.raise_for_status()
        return response.json()

    except requests.RequestException as error:
        return {
            "ok": False,
            "message": "Could not connect to TouchDesigner.",
            "error": str(error),
        }

    except ValueError as error:
        return {
            "ok": False,
            "message": "TouchDesigner returned an invalid response.",
            "error": str(error),
        }


@mcp.tool()
def list_saved_looks() -> list[str]:
    """List all saved visual presets."""
    return list_looks()


@mcp.tool()
def set_look(name: str, seconds: float = 3.0) -> dict:
    """Apply a saved visual look immediately.

    Available looks: neon, warm, cold, mono, dream.
    The seconds argument is retained for compatibility.
    """
    name = name.lower().strip()

    try:
        settings = get_look(name)
    except (KeyError, ValueError) as error:
        return {
            "ok": False,
            "message": f"Unknown look: {name}",
            "error": str(error),
        }

    previous_look = get_status().get("current_look")

    result = send_to_touchdesigner("look", {"name": name})

    if not result.get("ok", False):
        return {
            "ok": False,
            "message": "TouchDesigner could not apply the look.",
            "touchdesigner": result,
        }

    if previous_look and previous_look != name:
        set_current_look(name)

    return {
        "ok": True,
        "message": f"Applied look: {name}",
        "current_look": name,
        "settings": settings,
        "touchdesigner": result,
    }


@mcp.tool()
def set_intensity_tool(value: float) -> dict:
    """Set visual distortion intensity between 0.0 and 1.0."""

    if not 0.0 <= value <= 1.0:
        return {
            "ok": False,
            "message": "Intensity must be between 0.0 and 1.0.",
        }

    result = send_to_touchdesigner(
        "intensity",
        {"value": float(value)},
    )

    if not result.get("ok", False):
        return result

    try:
        set_intensity(value)
    except (TypeError, ValueError):
        pass

    return {
        "ok": True,
        "intensity": result.get("intensity", value),
        "message": f"Intensity set to {value}",
        "touchdesigner": result,
    }


@mcp.tool()
def set_glow_tool(value: float) -> dict:
    """Set Bloom glow intensity between 0.0 and 3.0."""

    if not 0.0 <= value <= 3.0:
        return {
            "ok": False,
            "message": "Glow must be between 0.0 and 3.0.",
        }

    result = send_to_touchdesigner(
        "glow",
        {"value": float(value)},
    )

    if not result.get("ok", False):
        return result

    return {
        "ok": True,
        "glow": result.get("glow", value),
        "message": f"Glow set to {value}",
        "touchdesigner": result,
    }


@mcp.tool()
def trigger_moment(name: str) -> dict:
    """Trigger a performance moment: drop, calm, or flash."""

    moment = name.lower().strip()
    allowed = {"drop", "calm", "flash"}

    if moment not in allowed:
        return {
            "ok": False,
            "message": "Unsupported moment. Choose drop, calm, or flash.",
        }

    result = send_to_touchdesigner(
        "moment",
        {"name": moment},
    )

    if not result.get("ok", False):
        return result

    return {
        "ok": True,
        "moment": moment,
        "message": f"Triggered performance moment: {moment}",
        "touchdesigner": result,
    }


@mcp.tool()
def recall_previous_look() -> dict:
    """Restore the previously selected visual look."""

    try:
        name = recall_last_look()
        settings = get_look(name)
    except (KeyError, ValueError) as error:
        return {
            "ok": False,
            "message": "Could not find the previous look.",
            "error": str(error),
        }

    result = send_to_touchdesigner(
        "look",
        {"name": name},
    )

    if not result.get("ok", False):
        return {
            "ok": False,
            "message": "TouchDesigner could not restore the previous look.",
            "current_look": name,
            "settings": settings,
            "touchdesigner": result,
        }

    set_current_look(name)

    return {
        "ok": True,
        "current_look": name,
        "settings": settings,
        "message": f"Restored previous look: {name}",
        "touchdesigner": result,
    }


@mcp.tool()
def get_stagehand_status() -> dict:
    """Get the current look, intensity, and palette."""
    return get_status()


if __name__ == "__main__":
    # Start the MCP server using Streamable HTTP.
    mcp.run(transport="streamable-http")
