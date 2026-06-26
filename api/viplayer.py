from api.theme import ThemeAPI 
from api.ui import UIAPI

class ViPlayerAPI:
    def __init__(self, app):
        self.theme = ThemeAPI(app)
        self.ui = UIAPI(app)

