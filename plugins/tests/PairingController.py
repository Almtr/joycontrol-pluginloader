import logging
from JoycontrolPlugin import JoycontrolPlugin

logger = logging.getLogger(__name__)

class PairingController(JoycontrolPlugin):
    async def run(self):
        # Press the A button when the controller is ready for input.
        logger.info('Pairing completed.')
        await self.button_push('a') # exit