import pyautogui

# Author: Dylan Poll

class mouseController(object): # https://pyautogui.readthedocs.io/en/latest/mouse.html
    def __init__(self) -> None:
        super().__init__()
    
    def mouseUp(self):
        pyautogui.moveRel(0, -30, duration = 0.01)

    def mouseDown(self):
        pyautogui.moveRel(0, 30, duration = 0.01)

    def mouseLeft(self):
        pyautogui.moveRel(-30, 0, duration = 0.01)

    def mouseRight(self):
        pyautogui.moveRel(30, 0, duration = 0.01)

    def mouseLeftClick(self):
        pyautogui.click()

    def mouseRightClick(self):
        pyautogui.rightClick()

    def mouseMiddleClick(self):
        pyautogui.middleClick()

class keyboardController(object): # https://pyautogui.readthedocs.io/en/latest/keyboard.html#the-press-keydown-and-keyup-functions
    def __init__(self) -> None:
        super().__init__()

    def keyboardMessage(self, TextMessage):
        pyautogui.typewrite(TextMessage) # prints a passed message.

    def enterKey(self):
        pyautogui.press('enter')

    def escapeKey(self):
        pyautogui.press('escape')
    
    def backspaceKey(self):
        pyautogui.press('backspace')

    def spaceKey(self):
        pyautogui.press('space')

# print(pyautogui.size()) # get the total screen size...
# pyautogui.moveTo(100, 100, duration = 1) # move to this position from where you are with a speed of 1 second...
# pyautogui.moveRel(0, 30, duration = 1) # relationally move position from current position...
# print(pyautogui.position()) # prints out the current mouse location.

# pyautogui.click(pyautogui.position()) # clicks at the current pointer position, can also just take in a x and y val
# pyautogui.click(100,100) # like this
# pyautogui.moveTo(1000, 1000, duration = 1) # moves mouse to 1000, 1000.
# pyautogui.dragRel(100, 0, duration = 1) # drags mouse 100, 0 relative to its previous position, thus dragging it to 1100, 1000
# pyautogui.dragRel(0, 100, duration = 1)
# pyautogui.dragRel(-100, 0, duration = 1)
# pyautogui.dragRel(0, -100, duration = 1)

# pyautogui.typewrite("typed out using python") # how to print out a message
# pyautogui.typewrite(["a", "left", "ctrlleft"]) # keypress approach
# pyautogui.hotkey("ctrlleft", "a") # key combo setup

# keyboard_keys :
# ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
# ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
# '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
# 'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
# 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
# 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
# 'browserback', 'browserfavorites', 'browserforward', 'browserhome',
# 'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
# 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
# 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
# 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
# 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
# 'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
# 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
# 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
# 'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
# 'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
# 'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
# 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
# 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
# 'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
# 'command', 'option', 'optionleft', 'optionright']