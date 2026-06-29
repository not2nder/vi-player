def down(app, motion):
    if app.mpv.isempty:
        return

    return min(app.mpv.count, app.cursor+motion.count)

def up(app, motion):
    if app.mpv.isempty:
        return
    
    return max(0, app.cursor-motion.count)

def start(app, motion):
    if app.mpv.isempty:
        return
    
    return motion.count-1

def end(app, motion):
    if app.mpv.isempty:
        return
    if motion.count > 1:
        return motion.count-1

    return app.mpv.count-1

def percent(app, motion):
    if app.mpv.isempty:
        return
    pct = min(motion.count,99)/100
    return int(app.mpv.count * pct)

def current(app, motion):
    if app.mpv.isempty:
        return

    return app.cursor + motion.count -1

MOTIONS = {
    "j": down,
    "k": up,
    "gg": start,
    "G": end,
    "%": percent,
    "_": current
}


