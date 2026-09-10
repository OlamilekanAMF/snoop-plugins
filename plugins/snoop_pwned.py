"""
snoop_pwned.py — HaveIBeenPwned Breach & Password Sentinel Plugin for Snoop OS
"""

import hashlib
import json
import urllib.request
import urllib.parse

__plugin_name__ = "snoop-pwned"
__version__ = "1.0.0"


def check_email_breach(email: str) -> str:
    email = email.strip().lower()
    if not email or "@" not in email:
        return "Invalid email address provided."

    encoded = urllib.parse.quote(email)
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{encoded}?truncateResponse=false"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Snoop-AI-Assistant/1.0",
            "Accept": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=8) as res:
            data = json.loads(res.read().decode("utf-8"))
            count = len(data)
            names = [b.get("Name", "Unknown") for b in data[:5]]
            sample = ", ".join(names)
            return (
                f"🚨 [BREACH ALERT] Email '{email}' was found in {count} known data breaches: "
                f"{sample}. You should immediately rotate passwords on these accounts."
            )
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return f"✅ [CLEAN] Good news! Email '{email}' was not found in any known public data breaches."
        elif e.code == 401:
            return "HaveIBeenPwned API key required for full enterprise account lookups. Use password audit freely."
        return f"HIBP lookup error (HTTP {e.code})."
    except Exception as e:
        return f"HIBP lookup connection failed: {e}"


def check_password_pwned(password: str) -> str:
    """Checks password safety using HaveIBeenPwned k-Anonymity SHA-1 API.
    Zero plaintext password ever touches the network."""
    if not password:
        return "No password provided."

    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    req = urllib.request.Request(url, headers={"User-Agent": "Snoop-AI-Assistant/1.0"})

    try:
        with urllib.request.urlopen(req, timeout=8) as res:
            lines = res.read().decode("utf-8").splitlines()
            for line in lines:
                parts = line.split(":")
                if len(parts) == 2 and parts[0].strip() == suffix:
                    count = int(parts[1].strip())
                    return (
                        f"🚨 [COMPROMISED PASSWORD] This password has appeared {count:,} times "
                        f"in public data dumps! It is dangerously unsafe and must not be used."
                    )
            return "✅ [STRONG] This password was NOT found in any known public breach dumps."
    except Exception as e:
        return f"Password audit failed: {e}"


def on_snoop_created(snoop):
    pass


def on_user_message(text: str, snoop=None):
    lower = text.strip().lower()

    if lower.startswith("check email breach ") or lower.startswith("pwned email "):
        email = text.split(maxsplit=3)[-1].strip()
        return check_email_breach(email)

    if lower.startswith("audit password ") or lower.startswith("check password "):
        pwd = text.split(maxsplit=2)[-1].strip()
        return check_password_pwned(pwd)

    return None
