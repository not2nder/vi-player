class UIAPI:
    def __init__(self, app):
        self.app = app

    def message(self, text):
        self.app.message = text
        self.app.dirty = True
