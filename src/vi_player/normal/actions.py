from vi_player.core.enums import Mode, Key, PlaybackState

def play(app):
    app.mpv.current = app.cursor
    app.mpv.play()

def pause(app):
    if app.mpv.isempty:
        return

    app.mpv.pause()

def seek_forward(app):
    app.mpv.jump(10)

def seek_back(app):
    app.mpv.jump(-10)

def seek_home(app):
    app.mpv.seek_start()

def seek_end(app):
    app.mpv.seek_end()

def volume_up(app):
    app.mpv.volumeup()

def volume_down(app):
    app.mpv.volumedown()

def mute(app):
    app.mpv.mute()

def next_song(app):
    if app.mpv.isempty:
        return

    if app.mpv.state == PlaybackState.WAITING:
        return

    app.mpv.next()
    app.cursor = app.mpv.current

def prev_song(app):
    if app.mpv.isempty:
        return

    if app.mpv.state == PlaybackState.WAITING:
        return
    
    app.mpv.prev()
    app.cursor = app.mpv.current

def enter_command(app):
    app.mode = Mode.COMMAND
    app.command.text = ":"
    app.message = ""

def clear_command(app):
    app.pending.clear()
    app.input.clear()
    app.input.clear_display()

def paste(app):
    count = app.mpv.playlist.paste(app.cursor)
    app.cursor = app.cursor + count

def exit_player(app):
    app.exit()

ACTIONS = {
    "l": seek_forward,
    "h": seek_back,
    "H": seek_home,
    "L": seek_end,
    "m": mute,
    " ": pause,
    "n": next_song,
    "N": prev_song,


    ":": enter_command,
    "q": exit_player,

    "p": paste,
}

KEY_ACTIONS = {
    Key.ENTER: play,
    Key.ESC: clear_command,
    Key.UP: volume_up,
    Key.DOWN: volume_down
}
