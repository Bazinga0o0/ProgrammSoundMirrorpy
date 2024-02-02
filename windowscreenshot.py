import ctypes
import ctypes.wintypes as wintypes
from PIL import Image
import win32gui
import win32ui
import pygetwindow as gw

# Define necessary ctypes
gdi32 = ctypes.WinDLL('gdi32')
user32 = ctypes.WinDLL('user32')

# Constants
SRCCOPY = 0xCC0020
PW_RENDERFULLCONTENT = 0x00000002
# Structures for device context
class BITMAPINFOHEADER(ctypes.Structure):
    _fields_ = [
        ('biSize', wintypes.DWORD),
        ('biWidth', wintypes.LONG),
        ('biHeight', wintypes.LONG),
        ('biPlanes', wintypes.WORD),
        ('biBitCount', wintypes.WORD),
        ('biCompression', wintypes.DWORD),
        ('biSizeImage', wintypes.DWORD),
        ('biXPelsPerMeter', wintypes.LONG),
        ('biYPelsPerMeter', wintypes.LONG),
        ('biClrUsed', wintypes.DWORD),
        ('biClrImportant', wintypes.DWORD)
    ]

class BITMAPINFO(ctypes.Structure):
    _fields_ = [
        ('bmiHeader', BITMAPINFOHEADER),
        ('bmiColors', wintypes.DWORD * 3)
    ]

# Function to capture a specific window
def capture_window(hwnd):
    # Get the window rectangle
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bot = rect
    width = right - left
    height = bot - top

    # Create device context
    window_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(window_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    # Create a bitmap for saving the screenshot
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bitmap)

    # Use PrintWindow to capture the window
    result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), PW_RENDERFULLCONTENT)

    # Check if PrintWindow succeeded
    if result == 1:
        # Convert to PIL Image
        bmpinfo = save_bitmap.GetInfo()
        bmpstr = save_bitmap.GetBitmapBits(True)
        img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    else:
        img = None

    # Clean up
    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, window_dc)

    return img

# Main script
window_title = "Opera"  # Replace with your window's title
window = gw.getWindowsWithTitle(window_title)[0]

if window:
    hwnd = window._hWnd
    screenshot = capture_window(hwnd)
    if screenshot:
        screenshot.save("window_screenshot.png")
    else:
        print("Failed to capture the window")
else:
    print("Window not found")
