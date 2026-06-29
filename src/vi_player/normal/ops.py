def cut(app, index):
    if app.mpv.isempty:
        return 

    app.mpv.playlist.cut(index)

def yank(app, index):
    if app.mpv.isempty:
        return

    app.mpv.playlist.copy(index)

