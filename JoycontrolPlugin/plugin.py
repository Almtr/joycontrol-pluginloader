from JoycontrolPlugin.commands import JoycontrolCommands
from abc import abstractmethod

class JoycontrolPluginError(Exception):
    pass

class JoycontrolPlugin(JoycontrolCommands):
    def __init__(self, controller_state, options):
        super().__init__(controller_state)
        self.options = options

    @abstractmethod
    async def run(self):
        pass