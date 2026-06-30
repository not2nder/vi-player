# Compatibility

Vi-Player aims to support any terminal emulator capable of handling modern ANSI escape sequences.

The project is regularly tested on multiple Linux distributions and terminal emulators.

# Operating Systems

The table below lists the environments officially tested during development.

| Operating System |    Status    | 
| ---------------- | :----------: |
| Arch Linux       |   ✅ Tested   |
| Debian           |   ✅ Tested   |
| Termux (Android) |   ✅ Tested   |
| Ubuntu           | ⏳ Not tested |
| Fedora           | ⏳ Not tested |
| Windows          |   ⏳ Planned  |
| macOS            |   ⏳ Planned  |

# Terminal Emulators

Vi-Player communicates directly with the terminal using ANSI escape sequences.

The following terminal emulators have been tested.

| Terminal  |       Status      | 
| --------- | :---------------: |
| Kitty     | ✅ Fully supported | 
| Alacritty | ✅ Fully supported |
| Konsole   | ✅ Fully supported |
| WezTerm   | ✅ Fully supported |
| Xfce Terminal | ✅ Fully supported |

Support for additional terminals will be evaluated as the project evolves.

# Audio Backend

Vi-Player uses:

* MPV
* python-mpv

Both must be available for audio playback to work correctly.

# Unicode Support

Vi-Player supports Unicode filenames and titles.

Character alignment is handled using the `wcwidth` library to correctly render:

* accented characters;
* emoji;
* CJK (Chinese, Japanese and Korean) characters;
* other variable-width Unicode symbols.

# Reporting Compatibility Issues

If you encounter problems on an unsupported operating system or terminal emulator, please consider opening an issue describing:

* operating system and version;
* terminal emulator and version;
* Python version;
* MPV version;
* steps to reproduce the issue.

Compatibility reports are valuable and help improve support across different environments.
