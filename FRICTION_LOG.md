\# StageHand — Hackathon Friction Log



\## Task Attempted

Connect a Python MCP server to TouchDesigner and control visual presets through an MCP client.



\## Steps Taken

1\. Installed the Python dependencies and MCP SDK.

2\. Configured the MCP server to expose visual-control tools.

3\. Opened the TouchDesigner project and enabled its local web server.

4\. Connected the client, listed saved visual presets, and applied a preset.



\## Expected Result

The MCP client should connect to the server, discover available tools, and apply visual changes in TouchDesigner.



\## Actual Result

The local end-to-end workflow worked after troubleshooting server and port configuration issues.



\## Severity

Moderate.



\## Workaround Used

Checked port availability, identified an existing process using port 8000, and verified that TouchDesigner was listening on port 9980 before testing again.



\## Suggested Improvement

Provide beginner-friendly documentation for Streamable HTTP configuration, common port conflicts, service availability checks, and a simple end-to-end MCP testing example.



\## Additional Observation

The local MCP-to-TouchDesigner workflow was verified. Direct Alexa+ integration has not yet been verified.

