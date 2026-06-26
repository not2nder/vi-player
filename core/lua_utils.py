def to_lua(lua, obj):
    table = lua.table()

    for i, value in enumerate(values, start=1):
        table[i] = value

    return table
