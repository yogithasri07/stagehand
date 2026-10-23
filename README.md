# StageHand

**Voice- and text-controlled live visual performance for TouchDesigner using MCP.**

StageHand is a local project that connects user commands to a TouchDesigner visual setup through a Model Context Protocol (MCP) server. It provides a way to control supported visual parameters and trigger performance moments using typed commands or speech.

## Features

- Type commands through the terminal.
- Use speech input when internet-based speech recognition is available.
- Select supported visual looks: `neon`, `warm`, `cold`, `mono`, and `dream`.
- Adjust visual intensity.
- Adjust glow settings.
- Trigger supported performance moments: `drop`, `calm`, and `flash`.
- Check the current StageHand status.
- List available looks and recall the previous look.

## Architecture

User command (text or speech)`r`n    |`r`n    v`r`nVoice client (voice_client.py)`r`n    |`r`n    v`r`nMCP server (stagehand_server.py)`r`n    |`r`n    v`r`nTouchDesigner web server and visual project

## Requirements

- Windows
- Python
- TouchDesigner
- The Python dependencies required by this project
- A TouchDesigner project configured for StageHand

Speech recognition uses an online service, so speech input requires an internet connection. Typed commands can be used without speech recognition.

## Setup

1. Clone or download this repository.
2. Open PowerShell in the project directory.
3. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

4. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

5. Install the project's required Python packages. Check the project's dependency list or setup documentation for the exact packages.
6. Open the required TouchDesigner project and start its configured web server.
7. In one PowerShell window, start the MCP server:

   ```powershell
   python stagehand_server.py
   ```

8. In a second PowerShell window, activate the environment and start the client:

   ```powershell
   python voice_client.py
   ```

9. Follow the menu to type a command, use speech, view help, or quit.

## Project Files

- `stagehand_server.py` — MCP server and supported control tools
- `voice_client.py` — terminal client for text and speech commands
- `state_manager.py` — state management
- `test_state.py` — state-related tests
- `data/looks.json` — saved look configuration

## Testing

Run the state tests with:

```powershell
python test_state.py
```

## Limitations

- StageHand depends on a correctly configured TouchDesigner project and its local web server.
- Speech recognition requires internet access.
- Available commands and controls depend on the implementation and TouchDesigner setup.

## License

See [LICENSE](LICENSE).
