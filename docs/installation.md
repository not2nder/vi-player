# Installation

This guide describes how to install and run Vi-Player from source.

Future releases may provide native packages for common package managers. Until then, the recommended installation method is using a Python virtual environment.

# Requirements

Before installing Vi-Player, make sure the following software is available on your system.

| Dependency | Minimum Version       |
| ---------- | --------------------- |
| Python     | 3.11                  |
| MPV        | Latest stable version |

Vi-Player relies on **python-mpv**, which communicates with an existing MPV installation. Installing the Python package alone is **not** sufficient.

# Clone the Repository

```bash
git clone https://github.com/not2nder/vi-player.git
cd vi-player
```

# Create a Virtual Environment

It is recommended to isolate the project's dependencies.

```bash
python -m venv .venv
```

Activate it:

### Linux / macOS

```bash
source .venv/bin/activate
```

# Install the Project

Install Vi-Player in editable mode:

```bash
pip install -e .
```

This step only needs to be performed once.

# Running

Launch Vi-Player:

```bash
viplay
```

Open a specific music directory:

```bash
viplay ~/Music
```

Or execute the package directly:

```bash
python -m vi_player
```

Whenever you open a new terminal session, reactivate the virtual environment before running the player.

```bash
source .venv/bin/activate
```

# Updating

If the repository has already been cloned:

```bash
git pull
```

Then reinstall the editable package if new dependencies have been introduced:

```bash
pip install -e .
```

# Troubleshooting

## MPV not found

Make sure MPV is installed on your system.

Vi-Player requires both:

* the MPV executable
* the system library used by `python-mpv`

## Configuration directory

The first launch automatically creates:

```text
~/.config/vi-player/
```

If it does not exist after running the player, verify that the application started correctly and has permission to write to your home directory.

