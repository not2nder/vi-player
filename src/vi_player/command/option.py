import shlex

OPTIONS = {
    "relativenumber",
    "number"
}

ALIASES = {
    "rnu": "relativenumber",
    "nu": "number",
}

def get_alias(name):
    return ALIASES.get(name, name)

def set_option(app, option, action, value):
    if option not in OPTIONS:
        app.message = f"opção inválida: {option}"
        return

    if action == "toggle":
        current = app.config.get(option)
        app.config.set(option, not current)
        return

    app.config.set(option, value)

def cmd_set(app, args):
    if len(args) < 2:
        return

    text = " ".join(args)
    expr = text[5:]

    parse_option(app, expr)

def parse_value(name):
    if name.startswith("no"):
        return get_alias(name[2:]), "set", False

    if name.endswith("!"):
        return get_alias(name[:-1]), "toggle", None

    return get_alias(name), "set", True

def parse_option(app, expr):
    name = shlex.split(expr)[0]
    
    option, action, value = parse_value(name)

    set_option(app, option, action, value)

