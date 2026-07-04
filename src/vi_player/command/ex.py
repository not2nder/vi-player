from vi_player.core.theme import get_theme, set_theme
from vi_player.command.option import cmd_set 

def jump_to(app, args):
    if app.mpv.isempty:
        return

    if len(args) < 2:
        return

    app.mpv.skip(int(args[1]))
    app.cursor = app.mpv.current

def exit_player(app, args):
    app.exit()

def open_dir(app, args):
    if len(args) < 2:
        app.message = "No directory specified"
        return

    try:
        app.mpv.playlist.load_directory(args[1])
        app.message = f"Showing songs from: {args[1]}"
        app.cursor = 0
    except FileNotFoundError as e:
        app.message = str(e)

def add_dir(app, args):
    if len(args) < 2:
        app.message = "No directory specified"
        return

    count = app.mpv.playlist.add_dir(args[1])

    if count:
        app.message = f'{count} song(s) loaded' if count > 1 else 'Song loaded'
    else:
        app.message = 'Empty or invalid directory'

def clear_playlist(app, args):
    if app.mpv.isempty:
        app.message = "No songs to remove"
        return

    app.mpv.playlist.clear()
    app.message = "Playlist cleared"

def set_rnu(app, args):
    app.config.set_relativenumber()

def disable_rnu(app, args):
    app.config.set_relativenumber(False)

def set_colorscheme(app, args):
    if len(args) < 2:
        app.message = get_theme().meta['name']
        return

    try:
        set_theme(args[1])
    except Exception as e:
        app.message = str(e)

def set_cmd(app, args):
    if len(args) < 2:
        app.message = ":set <option>"
        return

    cmd_set(app, args)

EX_COMMANDS = {
    ":jump": jump_to,

    ":o": open_dir,
    ":add": add_dir,
    ":clear": clear_playlist, 

    ":set": set_cmd,

    ":colorscheme": set_colorscheme,
    ":q": exit_player,
}

