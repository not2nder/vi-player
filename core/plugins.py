from lupa import LuaRuntime
from api.viplayer import ViPlayerAPI

from pathlib import Path

class PluginHost:
    def __init__(self, app):
        self.app = app
        self.lua = LuaRuntime(unpack_returned_tuples=True)

        self.api = ViPlayerAPI(app)
        self.inject_api()

        self.plugins = {}

    def inject_api(self):
        vi = self.lua.table()

        vi.theme = self.lua.table()
        vi.theme.current = self.api.theme.current
        vi.theme.list = self.api.theme.list
        vi.theme.set = self.api.theme.set

        vi.ui = self.lua.table()
        vi.ui.message = self.api.ui.message

        self.lua.globals()["vi"] = vi

    def load_plugin(self, name, path):
        source = Path(path).read_text()
        self.plugins[name] = self.lua.execute(source)

    def to_lua(self, obj):
        table = self.lua.table()

        for i, item in enumerate(obj, start=1):
            table[i] = item

        return table

