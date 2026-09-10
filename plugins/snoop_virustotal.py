"""
snoop_virustotal.py — VirusTotal File Hash & URL Threat Inspector Plugin
"""

import hashlib
import json
import os
import urllib.request
from pathlib import Path

__plugin_name__ = "snoop-virustotal"
__version__ = "1.0.0"


def calculate_sha256(filepath: str) -> str | None:
    p = Path(filepath)
    if not p.is_file():
        return None
    h = hashlib.sha256()
    with open(p, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def scan_hash(file_hash: str) -> str:
    h = file_hash.strip().lower()
    api_key = os.environ.get("VIRUSTOTAL_API_KEY", "")

    if not api_key:
        return (
            f"🔍 VirusTotal SHA-256: {h}\n"
            f"Direct Report Link: https://www.virustotal.com/gui/file/{h}\n"
            f"(Note: To get inline engine stats, add VIRUSTOTAL_API_KEY to your environment)."
        )

    url = f"https://www.virustotal.com/api/v3/files/{h}"
    req = urllib.request.Request(
        url,
        headers={
            "x-apikey": api_key,
            "Accept": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode("utf-8"))
            stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
            malicious = stats.get("malicious", 0)
            suspicious = stats.get("suspicious", 0)
            harmless = stats.get("harmless", 0)
            undetected = stats.get("undetected", 0)
            total = malicious + suspicious + harmless + undetected

            if malicious > 0:
                return (
                    f"🚨 [MALWARE DETECTED] {malicious}/{total} security engines flagged this file as malicious! "
                    f"Report: https://www.virustotal.com/gui/file/{h}"
                )
            return f"✅ [CLEAN] 0/{total} security engines flagged this hash. File appears safe."
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return f"ℹ️ Hash {h} is not yet seen by VirusTotal database. Upload via web: https://www.virustotal.com"
        return f"VirusTotal API error (HTTP {e.code})."
    except Exception as e:
        return f"VirusTotal connection error: {e}"


def on_snoop_created(snoop):
    pass


def on_user_message(text: str, snoop=None):
    lower = text.strip().lower()

    if lower.startswith("vt scan file ") or lower.startswith("scan file hash "):
        path = text.split(maxsplit=3)[-1].strip().strip('"').strip("'")
        h = calculate_sha256(path)
        if not h:
            return f"File not found: {path}"
        return scan_hash(h)

    if lower.startswith("vt scan hash ") or lower.startswith("scan hash "):
        h = text.split(maxsplit=3)[-1].strip()
        return scan_hash(h)

    return None
