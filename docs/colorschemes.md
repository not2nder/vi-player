# Colorschemes

Vi-Player supports customizable colorschemes through `.toml` files, allowing the appearance of the interface to be fully customized.

Each colorscheme is composed of four sections:

* **Meta** — Theme metadata
* **Palette** — Color definitions
* **Highlights** — Interface styling
* **Fillchars** — Characters used to fill empty areas of the interface

# Theme Directory

Colorschemes are loaded from:

```text
~/.config/vi-player/themes/
```

The repository already includes a collection of bundled themes. To install them, simply copy the contents of:

```text
src/vi_player/assets/themes/
```

into:

```text
~/.config/vi-player/themes/
```

Example:

```text
~/.config/vi-player/themes/
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

# Changing the Active Theme

The active colorscheme can be changed at any time while Vi-Player is running.

Use the following command:

```text
:colorscheme THEME
```

Where `THEME` is the filename without the `.toml` extension.

Example:

```text
:colorscheme nord
```

loads:

```text
themes/nord.toml
```

If the requested theme cannot be found, Vi-Player automatically falls back to the default colorscheme.

The default theme loaded during startup can also be configured through `config.json`. See the Configuration documentation for more information.

# Theme Structure

Every colorscheme follows the same TOML structure.

```toml
[meta]
name = "nord"
author = "Arctic Ice Studio"

[palette]
background = "#2E3440"
foreground = "#D8DEE9"
accent = "#88C0D0"
surface = "#3B4252"

cyan = "#8FBCBB"
green = "#A3BE8C"

muted = "#4C566A"
warning = "#D08770"

[highlight.Normal]
fg = "foreground"
bg = "background"

[highlight.CursorLine]
fg = "foreground"
bg = "surface"

[highlight.CursorBlock]
fg = "background"
bg = "cyan"

[highlight.LineNr]
fg = "muted"
bg = "background"

[highlight.CursorLineNr]
fg = "cyan"
bg = "background"

[highlight.StatusLine]
fg = "background"
bg = "accent"

[highlight.Muted]
fg = "muted"
bg = "background"

[highlight.Warning]
fg = "warning"
bg = "background"

[fillchars]
eob = "~"
```

---

# Meta

The `meta` section stores information about the theme.

```toml
[meta]
name = "my-theme"
author = "John Doe"
```

| Field    | Description  |
| -------- | ------------ |
| `name`   | Theme name   |
| `author` | Theme author |

These values are informational only and do not affect rendering.

# Palette

The `palette` section defines the colors available to the theme.

Each entry behaves like a named color variable that can later be referenced by highlight groups.

Example:

```toml
[palette]
background = "#14161B"
foreground = "#D8DAE2"
accent = "#A0D9A9"
surface = "#20242B"

green = "#A0D9A9"
blue = "#67BED9"

muted = "#4D5056"
warning = "#E69875"
```

The palette is not limited to a fixed number of colors.

Additional colors may be added whenever necessary.

For example:

```toml
purple = "#CBA6F7"
orange = "#FAB387"
red = "#F38BA8"
```

Unused colors are simply ignored by the renderer.

# Highlight Groups

Highlight groups define the appearance of individual interface elements.

Each group references colors previously declared in the palette.

Every highlight group must define both:

* `fg` — foreground color
* `bg` — background color

Example:

```toml
[highlight.Normal]
fg = "foreground"
bg = "background"
```

## Available Properties

| Property | Description | Default |
|----------|-------------|---------|
| `fg` | Foreground color | required |
| `bg` | Background color | required |
| `bold` | Render text in bold | `false` |
| `italic` | Render text in italic* | `false` |
| `reverse` | Swap foreground and background colors | `false` |
| `cursorblock` | Display the terminal cursor as a block while the highlight is active | `false` |

Current highlight groups are:

| Group          | Description                |
| -------------- | -------------------------- |
| `Normal`       | Default interface colors   |
| `CursorLine`   | Selected playlist row      |
| `LineNr`       | Playlist indexes           |
| `CursorLineNr` | Index of the selected row  |
| `StatusLine`   | Statusline                 |
| `Muted`        | Secondary text             |
| `Warning`      | Warning and error messages |

Example:

```toml
[highlight.StatusLine]
fg = "background"
bg = "accent"
```

Changes the appearance of the statusline using the colors defined in the palette.

# Fill Characters

Fill characters define the symbols used to represent empty regions of the interface.

Currently, Vi-Player provides one fill character:

| Name  | Description                                       |
| ----- | ------------------------------------------------- |
| `eob` | End-of-buffer marker displayed below the playlist |

Example:

```text
 1 Billie Jean
 2 Welcome to the Jungle
 3 Forever Young
~
~
~
```

The character can be customized:

```toml
[fillchars]
eob = "~"
```

or removed completely:

```toml
[fillchars]
eob = ""
```

---

# Creating a Custom Theme

The easiest way to create a new colorscheme is to duplicate one of the bundled themes.

Example:

```text
cp nord.toml my-theme.toml
```

Then:

1. Change the metadata.
2. Adjust the palette.
3. Update the highlight groups.
4. Save the file inside `~/.config/vi-player/themes/`.
5. Load it with:

```text
:colorscheme my-theme
```

---

# Bundled Themes

Vi-Player ships with a collection of colorschemes inspired by popular themes from the developer community.

Current bundled themes include:

* Catppuccin Mocha
* Dracula
* Everforest Dark
* Gruvbox
* Nord
* Nvim
* Rose Pine
* Solarized Dark
* Tokyo Night

Screenshots and previews of each colorscheme will be available in a future version of this documentation.

