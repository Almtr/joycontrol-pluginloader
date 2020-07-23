import logging
from JoycontrolPlugin import JoycontrolPlugin

logger = logging.getLogger(__name__)

class SimpleButtonMacro(JoycontrolPlugin):
    async def run(self):
        logger.info('Simple Button Macro Plugin')

        button_list = self.options
        logger.info(f'Button List {button_list}')

        for button in button_list:
            await self.button_push(button)
            await self.wait(1.0)