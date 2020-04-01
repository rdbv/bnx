
class Message:

    def __init__(self):
        self.messages = []

    def addError(self, text):
        self.messages.append((0, text))

    def addSuccess(self, text):
        self.messages.append((1, text))
