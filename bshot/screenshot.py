import numpy as np
import win32con
import win32gui
import win32ui


def get_offset(hwnd):
    x, y = win32gui.ClientToScreen(hwnd, (0, 0))
    x1, y1, _, _ = win32gui.GetWindowRect(hwnd)
    return x - x1, y - y1


def get_image_by_rect(hwnd, x, y, width=None, height=None):
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

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (width, height), dcObj, (x, y), win32con.SRCCOPY)
    bmInfo = dataBitMap.GetInfo()
    image = np.frombuffer(dataBitMap.GetBitmapBits(True), dtype=np.uint8)
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())
    image = image.reshape(bmInfo["bmHeight"], bmInfo["bmWidth"], 4)
    # bitmap has 4 channels like: BGRA. Discard Alpha
    image = image[:, :, :3]
    return image


def get_image(hwnd):
    return get_image_by_rect(hwnd, 0, 0)
