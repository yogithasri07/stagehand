
import asyncio
import re
import speech_recognition as sr

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


MCP_URL = "http://127.0.0.1:8000/mcp"

SAVED_LOOKS = ["neon", "warm", "cold", "mono", "dream"]
SAVED_MOMENTS = ["drop", "calm", "flash"]


# --------------------------------------------------
# CALL A STAGEHAND MCP TOOL
# --------------------------------------------------

async def call_stagehand_tool(session, tool_name, arguments=None):
    if arguments is None:
        arguments = {}

    result = await session.call_tool(tool_name, arguments)

    if getattr(result, "isError", False):
        print("Stagehand reported an error.")

    for item in result.content:
        if hasattr(item, "text"):
            print(item.text)


# --------------------------------------------------
# UNDERSTAND COMMANDS
# Works for both typed and spoken commands
# --------------------------------------------------

def understand_command(text):
    command = text.lower().strip()
    command = command.replace("-", " ")
    command = command.replace("_", " ")
    command = " ".join(command.split())

    # STATUS
    status_commands = [
        "status",
        "check status",
        "stagehand status",
        "show status",
        "get status",
        "what is the status",
        "how is stagehand",
    ]

    if command in status_commands:
        return "get_stagehand_status", {}

    # SHOW SAVED LOOKS
    look_list_commands = [
        "looks",
        "show looks",
        "list looks",
        "show saved looks",
        "list saved looks",
        "available looks",
        "what looks are available",
        "show all looks",
    ]

    if command in look_list_commands:
        return "list_saved_looks", {}

    # RESTORE PREVIOUS LOOK
    restore_commands = [
        "restore",
        "restore look",
        "previous look",
        "restore previous look",
        "recall previous look",
        "go back",
        "undo look",
        "bring back previous look",
    ]

    if command in restore_commands:
        return "recall_previous_look", {}

    # CHANGE LOOK
    for look in SAVED_LOOKS:
        look_commands = [
            look,
            f"{look} look",
            f"set {look}",
            f"set {look} look",
            f"show {look}",
            f"show {look} look",
            f"change to {look}",
            f"switch to {look}",
            f"activate {look}",
            f"apply {look}",
            f"use {look}",
            f"turn on {look}",
        ]

        if command in look_commands:
            return "set_look", {
                "name": look,
                "seconds": 3.0,
            }

    # SET INTENSITY
    intensity_match = re.search(
        r"(?:set |change |adjust )?intensity(?: to)?\s+(\d+(?:\.\d+)?)",
        command,
    )

    if intensity_match:
        value = float(intensity_match.group(1))

        if 0 <= value <= 1:
            return "set_intensity_tool", {"value": value}

        print("Intensity must be between 0 and 1.")
        return None, {}

    # SET GLOW
    glow_match = re.search(
        r"(?:set |change |adjust )?glow(?: to)?\s+(\d+(?:\.\d+)?)",
        command,
    )

    if glow_match:
        value = float(glow_match.group(1))

        if value >= 0:
            return "set_glow_tool", {"value": value}

        print("Glow cannot be negative.")
        return None, {}

    # TRIGGER SAVED MOMENTS
    for moment in SAVED_MOMENTS:
        moment_commands = [
            moment,
            f"trigger {moment}",
            f"play {moment}",
            f"start {moment}",
            f"activate {moment}",
            f"run {moment}",
            f"perform {moment}",
        ]

        if command in moment_commands:
            return "trigger_moment", {"name": moment}

    # HELP
    help_commands = [
        "help",
        "commands",
        "show commands",
        "list commands",
        "what can you do",
        "voice commands",
    ]

    if command in help_commands:
        print_available_commands()
        return None, {}

    return None, {}


# --------------------------------------------------
# DISPLAY AVAILABLE COMMANDS
# --------------------------------------------------

def print_available_commands():
    print("""
==================================================
             STAGEHAND COMMANDS
==================================================

STATUS
  status
  check status
  show status

SAVED LOOKS
  looks
  show saved looks
  list looks

CHANGE LOOK
  neon
  warm
  cold
  mono
  dream
  switch to warm
  set neon look

INTENSITY
  intensity 0.5
  set intensity to 0.8
  change intensity to 0.3

GLOW
  glow 1.5
  set glow to 2
  change glow to 0.5

SAVED MOMENTS
  drop
  calm
  flash
  trigger drop
  play flash

RESTORE
  restore
  restore previous look
  recall previous look
  go back

OTHER
  help
  commands

==================================================
""")


# --------------------------------------------------
# LISTEN TO THE MICROPHONE
# --------------------------------------------------

def listen_for_command():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("\nListening... Speak your command.")

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5,
            )

            try:
                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=6,
                )
            except sr.WaitTimeoutError:
                print("No speech detected. Please try again.")
                return None

        print("Recognizing speech...")

        spoken_text = recognizer.recognize_google(audio)
        print("You said:", spoken_text)

        return spoken_text

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return None

    except sr.RequestError as error:
        print("Speech recognition service error:", error)
        print("Check your internet connection.")
        return None

    except Exception as error:
        print("Microphone error:", error)
        print("You can select Type mode to continue.")
        return None


# --------------------------------------------------
# GET COMMAND USING TYPE OR SPEAK MODE
# --------------------------------------------------

async def get_user_command():
    while True:
        print("""
==================================================
             STAGEHAND CONTROL
==================================================
  1. Type a command
  2. Speak a command
  H. Show available commands
  Q. Quit
==================================================
""")

        try:
            choice = input("Choose Type, Speak, Help, or Quit (1/2/H/Q): ")
        except (EOFError, KeyboardInterrupt):
            return None

        choice = choice.strip().lower()

        if choice in ("q", "quit", "exit"):
            return None

        if choice in ("h", "help"):
            print_available_commands()
            continue

        if choice in ("1", "type", "text", "keyboard"):
            try:
                command = input(
                    "\nType your StageHand command: "
                ).strip()
            except (EOFError, KeyboardInterrupt):
                return None

            if command.lower() in ("q", "quit", "exit"):
                return None

            if command:
                return command

            print("Please enter a command.")
            continue

        if choice in ("2", "speak", "voice", "microphone"):
            command = await asyncio.to_thread(listen_for_command)

            if command:
                return command

            print("Try speaking again or select Type mode.")
            continue

        print("Invalid choice. Enter 1, 2, H, or Q.")


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

async def main():
    print("\nConnecting to StageHand MCP...")

    try:
        async with streamablehttp_client(MCP_URL) as (
            read_stream,
            write_stream,
            _,
        ):
            async with ClientSession(
                read_stream,
                write_stream,
            ) as session:

                await session.initialize()

                print("\nConnected to StageHand successfully!")

                tools_result = await session.list_tools()

                print("\nAvailable MCP tools:")
                for tool in tools_result.tools:
                    print("-", tool.name)

                print_available_commands()

                while True:
                    command_text = await get_user_command()

                    if command_text is None:
                        print("\nStageHand control stopped.")
                        break

                    tool_name, arguments = understand_command(
                        command_text
                    )

                    if tool_name is None:
                        print(
                            "Command not recognized or no action needed. "
                            "Choose H for help."
                        )
                        continue

                    print("\nCommand:", command_text)
                    print("Calling StageHand tool:", tool_name)
                    print("Arguments:", arguments)

                    try:
                        await call_stagehand_tool(
                            session,
                            tool_name,
                            arguments,
                        )

                        print("\nCommand processed.")

                    except Exception as error:
                        print("StageHand tool call failed:", error)

    except Exception as error:
        print("\nCould not connect to StageHand MCP.")
        print("Make sure stagehand_server.py is running.")
        print("Error:", error)


# --------------------------------------------------
# START PROGRAM
# --------------------------------------------------

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStageHand control stopped.")
