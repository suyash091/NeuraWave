from pyautogui import press, typewrite, hotkey, position
while True:
    press('a')
    typewrite('quick brown fox')
    hotkey('ctrl', 'w')
    print(position())

