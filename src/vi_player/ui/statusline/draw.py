from vi_player.ui.statusline.widgets import * 
from vi_player.util.pretty import length, padding, truncate, paint 

def render(screen, app):
    theme = get_theme()

    statusline = app.config.statusline
    separator = statusline.get("separator", "")

    left = [
        WIDGETS[item](app)
        for item in statusline.get("left", [])
        if item in WIDGETS
    ]
 
    right = (
        WIDGETS[item](app)
        for item in statusline.get("right", [])
        if item in WIDGETS
    )

    style = theme.style("StatusLine")

    line = build_statusline(left, right, separator, screen.width, style)

    screen.draw(screen.height - 1, line)

def build_statusline(left, right, separator, width, style):
    left_text  = separator.join(padding(t) for t in left if t)
    right_text = separator.join(padding(t) for t in right if t)

    gap = width - length(left_text) - length(right_text)
    gap = max(0, gap)
    space = ' ' * gap
    
    text = left_text + space + right_text
    text = truncate(text, width)

    return paint(
        text,
        style
    )

