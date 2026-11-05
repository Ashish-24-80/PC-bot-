import pyautogui
import time
import pyperclip

appname = "calculator"
pyperclip.copy(appname)

print("Pressing win")
pyautogui.press('win')
time.sleep(1)

print("Pasting")
pyautogui.hotkey('ctrl', 'v')
time.sleep(1)

print("Pressing enter")
pyautogui.press('enter')
