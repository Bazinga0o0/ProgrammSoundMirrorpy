import sounddevice as sd
import tkinter as tk

def stream_callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata 

def find_device_id(device_name):
    devices = sd.query_devices()
    devicein = None
    deviceout = None
    out = devices[sd.default.device[1]]['name']
    print(devices)
    for device_id, device_info in enumerate(devices):
        if device_name in device_info['name']:
            devicein = device_id
            break
    for device_id, device_info in enumerate(devices):
        if out in device_info['name']:
            deviceout = device_id
            if device_id >9:
                if device_info['hostapi'] == 1:
                    break

    if devicein is not None and deviceout is not None:

        return devicein, deviceout
    else:
        raise ValueError(f"Gerät mit dem Namen '{device_name}' nicht gefunden")

input_device_id = find_device_id("CABLE Output (VB-Audio Virtual Cable)")


device = input_device_id

samplerate = 44100 
channels = 2

# Create a tkinter window
root = tk.Tk()
root.title("Streaming Sound")

# Add a label to the window
label = tk.Label(root, text=f"Stream gestartet, fenster schließen um zu beenden. Geräte: {device}")
label.pack()

# Start the stream when the window is opened
with sd.Stream(callback=stream_callback, samplerate=samplerate, channels=channels, device=device):
    root.mainloop()