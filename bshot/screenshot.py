import numpy as np
import win32con
import win32gui
import win32ui


def get_image_by_rect(hwnd, x, y, width, height):
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


def get_image(child):
    c_x, c_y, c_x1, c_y1 = win32gui.GetWindowRect(child)
    w, h = c_x1 - c_x, c_y1 - c_y
    if c_x < 0 or c_y < 0 or c_x1 < 0 or c_y1 < 0:
        return None
    return get_image_by_rect(child, 0, 0, w, h)
