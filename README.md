# StageHand

**An Alexa-first voice interaction system for controlling live TouchDesigner visuals through the Model Context Protocol (MCP).**

## Overview

StageHand aims to make live visual performance more intuitive by allowing performers to control TouchDesigner visuals through voice interactions. Alexa/Alexa+ is the intended primary interaction layer, with StageHand connecting supported control actions to the visual environment.

## Problem

Live visual performances often require manual adjustment of visual parameters during a performance. Switching between controls can interrupt the creative flow and make spontaneous interaction difficult.

## Solution

StageHand is designed to connect voice-driven interaction with live visual control. The intended architecture uses Alexa/Alexa+ for interaction, a StageHand MCP server for exposing supported actions, and TouchDesigner for rendering the visuals.

A Python development client currently provides typed and microphone-based command testing while the Alexa integration is developed and verified.

## Architecture

```text
Alexa / Alexa+
      |
      v
StageHand Integration Layer
      |
      v
StageHand MCP Server
      |
      v
TouchDesigner Web Server
      |
      v
Live Visual Output
```

The diagram represents the intended architecture. The Alexa integration layer must be implemented and verified before this can be considered a complete working flow.

## Current Features

- Saved visual looks: `neon`, `warm`, `cold`, `mono`, and `dream`
- Intensity control
- Glow control, where supported by the connected TouchDesigner implementation
- Performance moments: `drop`, `calm`, and `flash`
- Previous-look recall
- MCP tools for supported control actions
- Typed and microphone-based development testing

## Technology Stack

- Python
- Model Context Protocol (MCP)
- TouchDesigner
- SpeechRecognition for the development voice client
- Alexa/Alexa+ as the intended primary interaction layer

## Setup

### Requirements

- Python installed on your system
- TouchDesigner installed
- The StageHand repository
- Internet access for Google's online speech-recognition service when using microphone mode

### Installation

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

### Running StageHand

1. Open TouchDesigner and configure its web server to accept StageHand requests.
2. In the first terminal, activate the virtual environment and start the MCP server:

```powershell
python stagehand_server.py
```

3. In a second terminal, navigate to the project folder, activate the same virtual environment, and start the development client:

```powershell
python voice_client.py
```

4. Use typed commands to test supported controls. Microphone mode requires internet access for Google's online speech recognition.

## Testing

Run the state manager test:

```powershell
python test_state.py
```

Check installed dependency consistency:

```powershell
python -m pip check
```

## Integration Status

The current Python development client uses Google's online speech-recognition service for microphone input. This is not an Alexa integration.

Alexa/Alexa+ is the intended primary interaction layer. Its actual connection to StageHand must be implemented and tested before it can be described as a working feature.

## Limitations

- Alexa/Alexa+ integration is not confirmed as implemented.
- Microphone recognition in the development client requires an internet connection.
- Visual controls depend on the running TouchDesigner project and its configured endpoints.
- Available actions are limited to the supported StageHand tools.

## Demo

Add a demonstration video or screenshots here once the complete workflow is recorded and verified.

## License

See the `LICENSE` file for licensing terms.
