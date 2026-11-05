from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def get_volume_interface():
    devices = AudioUtilities.GetSpeakers()
    # Try the high-level attribute first (common in newer pycaw versions)
    if hasattr(devices, 'EndpointVolume'):
        return devices.EndpointVolume
    
    # Fallback to the COM Activate method (case-insensitive check)
    activate_method = getattr(devices, 'Activate', getattr(devices, 'activate', None))
    if activate_method:
        interface = activate_method(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume))
    
    raise AttributeError("Could not find 'Activate' or 'EndpointVolume' on the audio device.")

async def handle_mute(update, context):
    try:
        vol = get_volume_interface()
        vol.SetMute(not vol.GetMute(None), None)
        await update.message.reply_text("Toggled mute.")
    except Exception as e:
        await update.message.reply_text(f"Failed to toggle mute: {e}")

async def handle_vol_up(update, context):
    try:
        vol = get_volume_interface()
        current = vol.GetMasterVolumeLevelScalar()
        vol.SetMasterVolumeLevelScalar(min(1.0, current + 0.1), None)
        await update.message.reply_text(f"Volume: {int(min(1.0, current+0.1)*100)}%")
    except Exception as e:
        await update.message.reply_text(f"Failed to increase volume: {e}")

async def handle_vol_down(update, context):
    try:
        vol = get_volume_interface()
        current = vol.GetMasterVolumeLevelScalar()
        vol.SetMasterVolumeLevelScalar(max(0.0, current - 0.1), None)
        await update.message.reply_text(f"Volume: {int(max(0.0, current-0.1)*100)}%")
    except Exception as e:
        await update.message.reply_text(f"Failed to decrease volume: {e}")

PLUGINS = [
    {"name": "Mute", "command": "mute", "description": "Toggle mute", "handler": handle_mute, "row": 3},
    {"name": "Vol+", "command": "vol_up", "description": "Volume up",  "handler": handle_vol_up,  "row": 3},
    {"name": "Vol-", "command": "vol_down","description": "Volume down","handler": handle_vol_down,"row": 3},
]
