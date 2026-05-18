import pyautogui
import time


DELAY_SECONDS = 4 * 60 * 60

print("Waiting 4 hours before pressing Enter...")
print("Leave this script running and switch focus to the window that should receive Enter.")
time.sleep(DELAY_SECONDS)
pyautogui.press("enter")
print("Enter key sent.")
