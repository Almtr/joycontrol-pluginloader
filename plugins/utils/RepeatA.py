import logging
from JoycontrolPlugin import JoycontrolPlugin

logger = logging.getLogger(__name__)

class RepeatA(JoycontrolPlugin):
    async def run(self):
        logger.info('Repeat A Plugin')

        while True:
            await self.button_push('a')
            await self.wait(0.1)