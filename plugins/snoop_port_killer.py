"""
snoop_port_killer.py — Rogue Process & Port Liberator Plugin for Snoop OS
"""

import psutil

__plugin_name__ = "snoop-port-killer"
__version__ = "1.0.0"


def find_process_on_port(port: int):
    for conn in psutil.net_connections(kind="inet"):
        if conn.laddr and conn.laddr.port == port:
            if conn.pid:
                try:
                    proc = psutil.Process(conn.pid)
                    return proc
                except Exception:
                    pass
    return None


def inspect_port(port_str: str) -> str:
    try:
        port = int(port_str.strip())
    except ValueError:
        return "Invalid port number. Specify an integer (e.g. 3000, 8080)."

    proc = find_process_on_port(port)
    if not proc:
        return f"✅ Port {port} is currently free. No active processes are listening on it."

    return (
        f"🔍 Port {port} is occupied by: '{proc.name()}' (PID: {proc.pid}, "
        f"Status: {proc.status()}). Say 'kill port {port}' to terminate it."
    )


def kill_port(port_str: str) -> str:
    try:
        port = int(port_str.strip())
    except ValueError:
        return "Invalid port number."

    if port in (80, 443, 135, 445):
        return f"⚠️ Safeguard: Refusing to kill critical Windows system port {port}."

    proc = find_process_on_port(port)
    if not proc:
        return f"Port {port} is already free."

    pname = proc.name()
    pid = proc.pid
    try:
        proc.terminate()
        proc.wait(timeout=3)
        return f"💥 Terminated process '{pname}' (PID: {pid}). Port {port} has been freed successfully!"
    except Exception:
        try:
            proc.kill()
            return f"💥 Force killed process '{pname}' (PID: {pid}). Port {port} is now free!"
        except Exception as e:
            return f"Failed to terminate process on port {port}: {e}"


def on_snoop_created(snoop):
    pass


def on_user_message(text: str, snoop=None):
    lower = text.strip().lower()

    if lower.startswith("who is using port ") or lower.startswith("check port "):
        port_val = text.split()[-1]
        return inspect_port(port_val)

    if lower.startswith("kill port ") or lower.startswith("free port "):
        port_val = text.split()[-1]
        return kill_port(port_val)

    return None
