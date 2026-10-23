\# StageHand — TouchDesigner Project



\## Overview



This folder contains the TouchDesigner project and visual assets used by StageHand, a voice- and text-controlled visual performance project.



StageHand connects a Python client to an MCP server, which communicates with TouchDesigner to control visual parameters and trigger performance effects.



\## Folder Contents



\- `StageHand.toe` — TouchDesigner project file.

\- `assets/neon.jpg` — Visual asset for the neon style.

\- `assets/warm.jpg` — Visual asset for the warm style.

\- `assets/cold and mono.jpg` — Visual asset for the cold and monochrome styles.

\- `assets/dream.jpg` — Visual asset for the dream style.



\## Requirements



\- TouchDesigner installed on your computer.

\- Python and the StageHand dependencies installed.

\- The StageHand MCP server and TouchDesigner web server configured as described in the main repository README.



\## How to Open the Project



1\. Clone or download the StageHand repository.

2\. Open TouchDesigner.

3\. Open `touchdesigner/StageHand.toe`.

4\. Check that the project loads without missing-file warnings.

5\. If the project uses external image assets, make sure the `assets` folder remains alongside the `.toe` file.

6\. Start the required TouchDesigner web server and StageHand MCP server using the instructions in the main README.

7\. Run the StageHand client and test the supported commands.



\## Visual Assets



The `assets` folder contains JPG images associated with the project's visual styles. These files are included as project resources.



If the project references these images, keep their filenames and relative folder locations unchanged. If an image is missing, check the file path in the relevant TouchDesigner Movie File In TOP.



\## Troubleshooting



\- \*\*Project does not open:\*\* Check that TouchDesigner is installed and the `.toe` file is accessible.

\- \*\*Missing image or texture:\*\* Confirm that the JPG files are present in `touchdesigner/assets/` and that the paths match the project.

\- \*\*Commands do not affect visuals:\*\* Verify that the TouchDesigner web server, MCP server, and StageHand client are running and configured correctly.

\- \*\*Voice input fails:\*\* Check your internet connection because the current speech-recognition setup uses online Google speech recognition.



\## Notes



This documentation describes the intended setup. Actual functionality depends on the saved TouchDesigner network, installed dependencies, and local configuration.



For the full project overview and Python setup, see the main repository `README.md`.



