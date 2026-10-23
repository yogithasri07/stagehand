
import json
from pathlib import Path

# Find the data folder inside the Stagehand project
DATA_FOLDER = Path(__file__).parent / "data"
LOOKS_FILE = DATA_FOLDER / "looks.json"

# Default visual presets
DEFAULT_LOOKS = {
    "neon": {
        "speed": 1.5,
        "scale": 1.2,
        "hue": 0.75,
        "glow": 0.9
    },
    "warm": {
        "speed": 0.8,
        "scale": 1.0,
        "hue": 0.08,
        "glow": 0.6
    },
    "cold": {
        "speed": 1.0,
        "scale": 1.1,
        "hue": 0.55,
        "glow": 0.7
    },
    "mono": {
        "speed": 0.7,
        "scale": 0.9,
        "hue": 0.0,
        "glow": 0.3
    },
    "dream": {
        "speed": 0.5,
        "scale": 1.4,
        "hue": 0.85,
        "glow": 1.0
    }
}


def load_state():
    """Load saved looks and performance state from JSON."""

    DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    if not LOOKS_FILE.exists():
        state = {
            "looks": DEFAULT_LOOKS,
            "current_look": "neon",
            "intensity": 50,
            "palette": "neon",
            "history": []
        }
        save_state(state)
        return state

    try:
        with LOOKS_FILE.open("r", encoding="utf-8") as file:
            state = json.load(file)

        # Add missing default looks without deleting user presets
        state.setdefault("looks", DEFAULT_LOOKS.copy())
        state.setdefault("current_look", "neon")
        state.setdefault("intensity", 50)
        state.setdefault("palette", "neon")
        state.setdefault("history", [])

        return state

    except (json.JSONDecodeError, OSError):
        raise RuntimeError(
            "Could not read data/looks.json. "
            "Check that it contains valid JSON."
        )


def save_state(state):
    """Save the current state to JSON."""

    DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    with LOOKS_FILE.open("w", encoding="utf-8") as file:
        json.dump(state, file, indent=4)


def list_looks():
    """Return the names of all saved visual presets."""

    state = load_state()
    return list(state["looks"].keys())


def get_look(name):
    """Return the settings for a particular look."""

    state = load_state()
    name = name.lower().strip()

    if name not in state["looks"]:
        raise ValueError(
            f"Unknown look '{name}'. Available looks: "
            + ", ".join(state["looks"].keys())
        )

    return state["looks"][name]


def set_current_look(name):
    """Remember the selected look and update history."""

    state = load_state()
    name = name.lower().strip()

    if name not in state["looks"]:
        raise ValueError(f"Unknown look: {name}")

    previous = state["current_look"]

    if previous != name:
        state["history"].append(previous)
        state["history"] = state["history"][-20:]

    state["current_look"] = name
    save_state(state)

    return state


def recall_last_look():
    """Return to the previously selected look."""

    state = load_state()

    if not state["history"]:
        return state["current_look"]

    previous = state["history"].pop()
    current = state["current_look"]

    state["current_look"] = previous
    state["history"].append(current)

    save_state(state)

    return previous


def set_intensity(value):
    """Save intensity from 0 to 100."""

    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Intensity must be a number between 0 and 100.")

    if not 0 <= value <= 100:
        raise ValueError("Intensity must be between 0 and 100.")

    state = load_state()
    state["intensity"] = value
    save_state(state)

    return value


def get_status():
    """Return the current performance state."""

    state = load_state()

    return {
        "current_look": state["current_look"],
        "intensity": state["intensity"],
        "palette": state["palette"]
    }
