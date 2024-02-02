import sounddevice as sd
def find_device_id(device_name, samplerate):
    devices = sd.query_devices()
    devicein = None
    deviceout = None
    if devices:
        print(devices[0].keys())
    out = devices[sd.default.device[1]]['name']
    for device_id, device_info in enumerate(devices):
        if device_name in device_info['name']:
            try:
                sd.check_input_settings(device=device_id, samplerate=samplerate)
                devicein = device_id
                print(f"Device '{device_name}' supports sample rate {samplerate}, deviceid: {device_id}")
            except sd.PortAudioError:
                print(f"Device '{device_name}' does not support sample rate {samplerate}")

    
    for device_id, device_info in enumerate(devices):
        if out in device_info['name']:
            try:
                sd.check_output_settings(device=device_id, samplerate=samplerate)
                deviceout = device_id
                print(f"Device '{out}' supports sample rate {samplerate}, deviceid: {device_id}")
            except sd.PortAudioError:
                print(f"Device '{out}' does not support sample rate {samplerate}")

    if devicein is not None and deviceout is not None:
        print(devicein, deviceout)
        return devicein, deviceout
    else:
        raise ValueError(f"Gerät mit dem Namen '{device_name}' nicht gefunden")

samplerate = 44100
input_device_id = find_device_id("CABLE Output (VB-Audio Virtual Cable)", samplerate)