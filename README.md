# Snoop Plugins — Community Marketplace

The official plugin repository for [Snoop AI](https://github.com/OlamilekanAMF).

## Install a plugin
Tell Snoop: `install plugin [plugin-name]`

## Browse plugins
Tell Snoop: `list available plugins`

## Submit your own plugin

1. Fork this repo
2. Add your `.py` file to the `plugins/` folder
3. Add your plugin entry to `plugins.json`:

```json
{
  "name":        "my-plugin",
  "description": "What it does in one line",
  "author":      "YourGitHubUsername",
  "version":     "1.0.0",
  "file":        "my_plugin.py",
  "tags":        ["category", "keyword"],
  "installs":    0
}
```

4. Open a Pull Request — approved plugins appear in the marketplace immediately.

## Plugin format

```python
# plugins/my_plugin.py

def on_snoop_created(snoop=None):
    """Called once when Snoop boots."""
    pass

def on_user_message(text, snoop=None):
    """
    Called before every user message.
    Return a string to override Snoop's response.
    Return None to let Snoop handle it normally.
    """
    if "my trigger phrase" in text.lower():
        return "My custom response"
    return None

def on_snoop_response(text, snoop=None):
    """Called after Snoop generates a response. Return string to modify it."""
    return text
```

## Available plugins

See `plugins.json` for the full list.
