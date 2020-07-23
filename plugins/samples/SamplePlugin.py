import logging
from JoycontrolPlugin import JoycontrolPlugin

logger = logging.getLogger(__name__)

class SamplePlugin(JoycontrolPlugin):
    async def run(self):
        logger.info('This is sample joycontrol plugin!')

        logger.info(f'Plugin Options: {self.options}')

        logger.info('Push the A Button')
        await self.button_push('a')
        await self.wait(0.3)

        logger.info('Tilt the left stick down')
        await self.left_stick('down')
        await self.wait(0.3)