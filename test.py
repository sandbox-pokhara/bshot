import cv2
import win32gui

from bshot.screenshot import get_image

hwnd = win32gui.FindWindow(None, "Untitled - Notepad")
img = get_image(hwnd, method="srccopy")

cv2.imshow("", img)
cv2.waitKey()
