import sounddevice as sd
import time
import dxcam
import cv2
import pygetwindow as gw
import pyautogui
import numpy as np
from PIL import ImageGrab
import ctypes
import ctypes.wintypes as wintypes
from PIL import Image
import win32gui
import win32ui
import pygetwindow as gw
import win32api

while True:
    try:
        app_name = input("Fenstername (input f for fullscreen): ")
        FPS = int(input("FPS: "))
        break
    except:
        print("Bitte eine Zahl eingeben")



def stream_callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata 

def find_device_id(device_name):
    devices = sd.query_devices()
    devicein = None
    deviceout = None
    out = devices[sd.default.device[1]]['name']
    for device_id, device_info in enumerate(devices):
        if device_name in device_info['name']:
            devicein = device_id
            break
    for device_id, device_info in enumerate(devices):
        if out in device_info['name']:
            deviceout = device_id
            if device_id > 9 and device_info['hostapi'] == 1:
                break

    if devicein is not None and deviceout is not None:
        return devicein, deviceout
    else:
        raise ValueError(f"Gerät '{device_name}' nicht gefunden")

device = find_device_id("CABLE Output (VB-Audio Virtual Cable)")

samplerate = 44100 
channels = 2

gdi32 = ctypes.WinDLL('gdi32')
user32 = ctypes.WinDLL('user32')

SRCCOPY = 0xCC0020
PW_RENDERFULLCONTENT = 0x00000002

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


def capture_window(hwnd, fs):
    
    # Get window dimensions
    rect = win32gui.GetWindowRect(hwnd)
    left, top, right, bot = rect
    width = right - left
    height = bot - top

    # Window
    window_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc = win32ui.CreateDCFromHandle(window_dc)
    save_dc = mfc_dc.CreateCompatibleDC()

    # Bitmap
    save_bitmap = win32ui.CreateBitmap()
    save_bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
    save_dc.SelectObject(save_bitmap)

    result = ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), PW_RENDERFULLCONTENT)

    if result == 1:

        bmpinfo = save_bitmap.GetInfo()
        bmpstr = save_bitmap.GetBitmapBits(True)
        img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)
    else:
        img = None

    win32gui.DeleteObject(save_bitmap.GetHandle())
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, window_dc)

    return img


with sd.Stream(callback=stream_callback, samplerate=samplerate, channels=channels, device=device):
    start_time = time.time()
    if app_name == "f":
        camera = dxcam.create(output_color="RGB")
        camera.start(target_fps=FPS, video_mode=True)
        while True:
            try:
                frame = camera.get_latest_frame()
                frame = np.array(frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                cv2.imshow("frame", frame)
            except Exception as e:
                print(e)
                print("Fenster nicht gefunden")
                break
            if cv2.waitKey(1) & 0xFF == 113 or cv2.getWindowProperty("frame", cv2.WND_PROP_VISIBLE) < 1:
                break

    else:
        while True:
            try:
                windows = gw.getWindowsWithTitle(app_name)
                if windows:
                    window = windows[0]
                    hwnd = window._hWnd
                    if hwnd is not None:
                        frame = capture_window(hwnd, False)
                        if frame is not None:
                            frame = np.array(frame)
                            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                            cv2.imshow("frame", frame)
            except Exception as e:
                print(e)
                print("Fenster nicht gefunden")
                break
            if cv2.waitKey(1) & 0xFF == 113 or cv2.getWindowProperty("frame", cv2.WND_PROP_VISIBLE) < 1:
                break



        end_time = time.time()
        elapsed_time = end_time - start_time
        sleep_time = max(1/FPS - elapsed_time, 0)

cv2.destroyAllWindows()
