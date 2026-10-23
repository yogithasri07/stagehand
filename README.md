# StageHand

**Voice- and text-controlled live visual performance for TouchDesigner using the Model Context Protocol (MCP).**

StageHand is a local project that connects user commands to a TouchDesigner visual setup through an MCP server. It lets users change supported visual looks, adjust intensity and glow settings, and trigger performance moments using typed commands or speech.

## Problem

Live visual performance often requires manually adjusting parameters while managing the performance itself. This can interrupt the creative workflow and make quick changes harder during a live session.

## Solution

StageHand provides a command-based interface for controlling supported TouchDesigner visuals. Users can type commands or use speech input to interact with the MCP server and control the connected visual setup.

## Features

- Type commands through the terminal.
- Use speech input when internet-based speech recognition is available.
- Select saved looks: `neon`, `warm`, `cold`, `mono`, and `dream`.
- Adjust visual intensity.
- Adjust glow settings.
- Trigger performance moments: `drop`, `calm`, and `flash`.
- Check the current StageHand status.
- List available looks and recall the previous look.

## Architecture

```text
User
 |
 | Typed or spoken command
 v
Voice Client (voice_client.py)
 |
 v
MCP Server (stagehand_server.py)
 |
 v
TouchDesigner Web Server
 |
 v
Live Visual Output
```

## Requirements

- Windows
- Python
- TouchDesigner
- Required Python dependencies
- A TouchDesigner project configured for StageHand

Speech recognition uses an online service and requires an internet connection. Typed commands can be used without online speech recognition.

## Setup

### 1. Get the project

Clone the repository or download the source code from GitHub.

```powershell
git clone https://github.com/yogithasri07/stagehand.git
cd stagehand
```

### 2. Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

Install the Python packages required by the project. Use the dependency list or setup instructions included in the repository, if available.

### 4. Start TouchDesigner

Open the StageHand TouchDesigner project and start its configured web server. Confirm that the TouchDesigner web server is reachable at:

`http://127.0.0.1:9980`

The project must be configured to accept the controls sent by StageHand.

### 5. Start the MCP server

Open a PowerShell window in the project directory, activate the virtual environment, and run:

```powershell
python stagehand_server.py
```

### 6. Start the client

Open a second PowerShell window in the project directory, activate the virtual environment, and run:

```powershell
python voice_client.py
```

Follow the terminal menu to type a command, use speech input, view help, or quit.

## Project Files

- `stagehand_server.py` — MCP server and supported control tools.
- `voice_client.py` — terminal client for text and speech commands.
- `state_manager.py` — state management.
- `test_state.py` — state-related tests.
- `data/looks.json` — saved look configuration.
- `touchdesigner/` — TouchDesigner project files, assets, and setup instructions.

## Testing

Run the state tests from the project directory:

```powershell
python test_state.py
```

## Limitations

- StageHand depends on a correctly configured TouchDesigner project and its local web server.
- Speech recognition requires internet access.
- Available commands and controls depend on the implementation and TouchDesigner setup.
- The current client uses a terminal interface.

## Demo

Add a link to your project demonstration video here when it is ready.

## License

See [LICENSE](LICENSE).
