
from state_manager import (
    load_state,
    list_looks,
    get_look,
    set_current_look,
    recall_last_look,
    set_intensity,
    get_status,
)

print("STAGEHAND STATE TEST")
print("--------------------")

state = load_state()
print("Initial status:", get_status())

print("\nAvailable looks:")
print(list_looks())

print("\nNeon look settings:")
print(get_look("neon"))

print("\nSwitching to warm...")
set_current_look("warm")
print(get_status())

print("\nSetting intensity to 80...")
set_intensity(80)
print(get_status())

print("\nReturning to the previous look...")
recall_last_look()
print(get_status())

print("\nTest complete!")
