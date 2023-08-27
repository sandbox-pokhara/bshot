from ctypes import windll

import numpy as np
import win32con
import win32gui
import win32ui

from bshot.exceptions import InvalidMethodException


def get_offset(hwnd):
    x, y = win32gui.ClientToScreen(hwnd, (0, 0))
    x1, y1, _, _ = win32gui.GetWindowRect(hwnd)
    return x - x1, y - y1


def get_image_by_rect(
    hwnd,
    x,
    y,
    method="windll",
    width=None,
    height=None,
):
    # if width/height is None, then use the size of the client area
    _, _, w, h = win32gui.GetClientRect(hwnd)
    if width is None:
        width = w
    if height is None:
        height = h

    # add offset to x, y to match the client area
    off_x, off_y = get_offset(hwnd)
    x += off_x
    y += off_y

    scaleFactor = windll.shcore.GetScaleFactorForDevice(0) / 100
    width = int(width * scaleFactor)
    height = int(height * scaleFactor)

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)

    if method == "windll":
        # windll method
        windll.user32.PrintWindow(hwnd, cDC.GetSafeHdc(), 2)
    elif method == "srcopy":
        # srcopy method
        cDC.BitBlt((0, 0), (width, height), dcObj, (x, y), win32con.SRCCOPY)
    else:
        raise InvalidMethodException(f"Method {method} is not valid.")

    bmInfo = dataBitMap.GetInfo()
    image = np.frombuffer(dataBitMap.GetBitmapBits(True), dtype=np.uint8)
    image = image.reshape(bmInfo["bmHeight"], bmInfo["bmWidth"], 4)
    # bitmap has 4 channels like: BGRA. Discard Alpha
    image = image[:, :, :3]

    win32gui.DeleteObject(dataBitMap.GetHandle())
    cDC.DeleteDC()
    dcObj.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)

    # Now you have the image data in the NumPy array format
    return image


def get_image(hwnd, method="windll"):
    return get_image_by_rect(hwnd, 0, 0, method)
