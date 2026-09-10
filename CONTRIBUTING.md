# Contributing a Plugin to Snoop OS

We welcome community plugins! Follow this guide to build, test, and publish your plugin.

---

## 1. Plugin Architecture

A Snoop plugin is a standalone Python file (`.py`) dropped into the user's `plugins/` directory. It uses lifecycle hooks:

```python
"""
snoop_my_plugin.py — Example Snoop Plugin
"""

__plugin_name__ = "snoop-my-plugin"
__version__ = "1.0.0"

def on_snoop_created(snoop):
    """Called once when Snoop boots."""
    pass

def on_user_message(text: str, snoop=None):
    """
    Called before every user voice/text prompt.
    Return a string to immediately answer and intercept processing.
    Return None to let Snoop handle it normally.
    """
    if text.strip().lower() == "my trigger":
        return "Response from my custom plugin!"
    return None

def on_snoop_response(text: str, snoop=None):
    """Called after Snoop generates a response to post-process output."""
    return text
```

---

## 2. Security Standards (AST Static Analysis)

When users install a plugin, Snoop automatically runs an **AST security scan**. Plugins containing the following will be **automatically rejected**:
- Calls to `os.system`, `os.popen`, `subprocess.run`, `subprocess.Popen`
- Calls to raw `eval()`, `exec()`, or dynamic `__import__`
- Insecure imports (`ctypes` usage must be strictly audited, `subprocess` is forbidden)

Please use safe standard libraries: `urllib.request`, `json`, `hashlib`, `psutil`, `socket`, `pathlib`.

---

## 3. How to Submit a Pull Request

1. Fork this repository: `github.com/OlamilekanAMF/snoop-plugins`.
2. Add your plugin source file into the `plugins/` folder (e.g. `plugins/snoop_my_plugin.py`).
3. Add your plugin manifest entry into `plugins.json`:
   ```json
   {
     "id": "snoop-my-plugin",
     "name": "snoop-my-plugin",
     "displayName": "My Custom Plugin",
     "description": "Short explanation of features.",
     "author": "your-github-username",
     "category": "Developer",
     "stars": 1,
     "installs": 0,
     "version": "1.0.0",
     "file": "snoop_my_plugin.py",
     "tags": ["custom", "productivity"],
     "isVerified": true,
     "installCommand": "snoop install plugin \"snoop-my-plugin\""
   }
   ```
4. Test that your plugin loads in your local Snoop:
   ```bash
   python -c "from skills.plugin_marketplace import _security_scan; print(_security_scan(open('plugins/snoop_my_plugin.py').read()))"
   ```
5. Submit your Pull Request. Once approved and merged, the plugin automatically appears on the Snoop website and is available to all users!
