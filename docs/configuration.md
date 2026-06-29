# Configuration

Vi-Player stores user preferences outside the project directory, allowing updates without overwriting personal settings.

All configuration files are automatically created the first time the player is launched.

---

# Configuration Directory

By default, Vi-Player stores its configuration in:

```text
~/.config/vi-player/
```

On the first launch, the default configuration files are copied to this directory automatically.

The expected structure is:

```text
~/.config/vi-player/
├── config.json
└── themes/
    ├── catppuccin-mocha.toml
    ├── dracula.toml
    ├── everforest-dark.toml
    ├── gruvbox.toml
    ├── nord.toml
    ├── nvim.toml
    ├── rose-pine.toml
    ├── solarized-dark.toml
    └── tokyo-night.toml
```

---

# Configuration File

The main configuration file is:

```text
config.json
```

Example:

```json
{
    "general": {
        "theme": "nord"
    },

    "player": {
        "relativenumbers": true,
        "number": true
    },

    "statusline": {
        "left": ["mode", "state"],
        "right": ["theme", "position"],

        "separator": "|"
    }
}
```

The file is organized into independent sections, making it easy to extend as new features become available.

---

# General Settings

The `general` section contains application-wide options.

## Theme

Defines the colorscheme loaded during startup.

```json
{
    "general": {
        "theme": "nord"
    }
}
```

The value must match one of the files inside:

```text
~/.config/vi-player/themes/
```

without the `.toml` extension.

For example:

```json
"theme": "nord"
```

loads `themes/nord.toml`

If the requested theme cannot be found, Vi-Player automatically falls back to the default colorscheme.

> See [`docs/colorschemes.md`](colorschemes.md) for the complete list of bundled themes and instructions for creating your own.

---

# Player Settings

The `player` section controls playlist behavior.

## Relative Numbers

Enable or disable Vim-style relative numbers.

```json
{
    "player": {
        "relativenumbers": true
    }
}
```

When enabled:

* the current line displays its absolute index;
* all other lines display the relative distance from the cursor.

This makes motions easier to read and execute.

For example:

```text
3j
```

moves three items down.

Likewise:

```text
3k
```

moves three items up.

---

## Numbers

Enable or disable indeces.

# Statusline

The statusline can be customized through the `statusline` section.

Example:

```json
{
    "statusline": {
        "left": ["mode", "state"],
        "right": ["theme", "position"],

        "separator": "|"
    }
}
```

The statusline is divided into two regions:

* **left**
* **right**

Each region accepts a list of modules.

Example:

```json
{
    "left": [
        "mode",
        "state",
        "song"
    ]
}
```

Modules are rendered in the same order they appear in the list.

---

## Available Modules

| Module     | Description         |
| ---------- | ------------------- |
| `mode`     | Current editor mode |
| `state`    | Playback state      |
| `song`     | Current song title  |
| `artist`   | Current artist      |
| `album`    | Current album       |
| `theme`    | Active colorscheme  |
| `position` | Cursor position     |
| `percent`  | Playlist progress   |

---

## Separator

The separator is placed between every rendered module.

Example:

```json
{
    "separator": "|"
}
```

Produces:

```text
NORMAL | PLAYING | Song Title
```

It may be replaced with any string.

Examples:

```text
•
```

```text
>>
```

```text
│
```

or even:

```text
—
```

---

# Future Configuration

The configuration system is designed to grow over time.

Future versions may introduce additional sections for:

* key mappings
* plugins
* layouts
* command aliases
* scripting
* user interface customization

while preserving backward compatibility with existing configuration files.

