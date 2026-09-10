"""
snoop_obs_director.py — OBS Studio WebSocket Director Plugin for Snoop OS
"""

import json
import socket

__plugin_name__ = "snoop-obs-director"
__version__ = "1.0.0"


def send_obs_command(request_type: str, request_data: dict | None = None, host="127.0.0.1", port=4455) -> str:
    payload = {
        "op": 6,  # Request opcode in OBS WebSocket protocol v5
        "d": {
            "requestType": request_type,
            "requestId": "snoop-obs-req",
            "requestData": request_data or {}
        }
    }

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2.5)
    try:
        s.connect((host, port))
        msg = json.dumps(payload) + "\n"
        s.sendall(msg.encode("utf-8"))
        res = s.recv(4096).decode("utf-8", errors="ignore")
        s.close()
        return f"🎬 [OBS Studio] Request '{request_type}' dispatched successfully."
    except ConnectionRefusedError:
        return "⚠️ OBS Studio is not running or WebSocket Server is disabled (Settings -> WebSocket Server -> Port 4455)."
    except Exception as e:
        return f"OBS Connection Error: {e}"


def on_snoop_created(snoop):
    pass


def on_user_message(text: str, snoop=None):
    lower = text.strip().lower()

    if lower in ("obs start recording", "start obs recording"):
        return send_obs_command("StartRecord")

    if lower in ("obs stop recording", "stop obs recording"):
        return send_obs_command("StopRecord")

    if lower in ("obs toggle recording", "toggle recording"):
        return send_obs_command("ToggleRecord")

    if lower.startswith("obs switch scene "):
        scene = text[17:].strip()
        return send_obs_command("SetCurrentProgramScene", {"sceneName": scene})

    if lower in ("obs mute mic", "mute streaming mic"):
        return send_obs_command("ToggleInputMute", {"inputName": "Mic/Aux"})

    return None
