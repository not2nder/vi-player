# <div align="center">Vi-Player</div>

<p align="center">
A terminal music player focused on speed, simplicity and keyboard-driven navigation. Inspired by the modal philosophy of Vim and designed for terminal-oriented workflows.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?logo=python" />
  <img src="https://img.shields.io/badge/License-GPLv3-green" />
</p>

---

## About

Vi-Player is a terminal music player written in Python that brings modal navigation concepts to music playback.

Inspired by tools such as Vim, Ranger, Cmus and Ncmpcpp, Vi-Player focuses on keyboard-driven interaction while maintaining its own workflow and interface tailored for media playback.

Rather than relying on graphical controls or mouse interaction, the player encourages a fast and predictable workflow built around motions, commands and keyboard navigation.

---

## Goals

* Fast navigation
* Modal interface
* Keyboard-driven workflow
* Customizable
* Open source
* Cross-platform

---

## Features

* Local music playback
* Modal navigation
* Vim-inspired motions
* Runtime command system
* Theme support
* Configurable interface

---

## Installation

### Requirements

Before installing Vi-Player, make sure the following dependencies are available on your system:

* Python 3.11+
* MPV

### Clone the repository

```bash
git clone https://github.com/not2nder/vi-player.git
cd vi-player
```

### Create a virtual environment

Create a virtual environment to isolate the project's dependencies.

```bash
python -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

Install the project:

```bash
pip install -e .
```

> The installation only needs to be performed once.

---

## Running

Start Vi-Player:

```bash
viplay
```

Open a specific music directory:

```bash
viplay ~/Music/MyPlaylist
```

Alternatively, the package can also be executed directly with Python:

```bash
python -m vi_player
```

Whenever you open a new terminal, activate the virtual environment before running the player again:

```bash
source .venv/bin/activate
viplay
```

> [!NOTE]
> The current installation method is intended for development. Future releases may be distributed through package managers or other installation methods, removing the need for a virtual environment.

---

## Getting Started

Currently, Vi-Player supports local music libraries containing **MP3** files.

### Modes

Vi-Player currently provides two primary modes:

| Mode        | Description                                |
| ----------- | ------------------------------------------ |
| **NORMAL**  | Playlist navigation and modal interactions |
| **COMMAND** | Execute commands starting with `:`         |

---

### Basic Motions

| Motion | Description                           |
| ------ | ------------------------------------- |
| `j`    | Move to the next item                 |
| `k`    | Move to the previous item             |
| `gg`   | Jump to the beginning of the playlist |
| `G`    | Jump to the end of the playlist       |
| `:`    | Enter Command mode                    |

Detailed information about motions, operators and counts is available in:

* [`docs/motions.md`](docs/motions.md)

---

### Basic Commands

| Command  | Description                                        |
| -------- | -------------------------------------------------- |
| `:o`     | Open a directory                                   |
| `:add`   | Add songs from a directory to the current playlist |
| `:clear` | Clear current playlist content                     |
| `:q`     | Quit Vi-Player                                     |

---

## Documentation

Additional documentation can be found in the `docs/` directory.

* Installation
* Configuration
* Motions and Operators
* Colorschemes

---

## Contributing

Vi-Player is under active development, and its architecture continues to evolve.

Bug reports, suggestions, discussions and pull requests are always welcome.

---

## License

This project is distributed under the **GNU General Public License v3.0 (GPL-3.0)**.

