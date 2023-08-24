# bshot

Python package to take screenshots of windows that are in background

## Installation

```
pip install bshot
```

## Usage

```python
import cv2
import win32gui

from bshot.screenshot import get_image

hwnd = win32gui.FindWindow(None, "Untitled - Notepad")
img = get_image(hwnd)
cv2.imshow("", img)
cv2.waitKey(0)
```

## Limitations

- `get_image` does not properly crop the contents of window
