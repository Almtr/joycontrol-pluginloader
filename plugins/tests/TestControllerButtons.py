import logging
from JoycontrolPlugin import JoycontrolPlugin

logger = logging.getLogger(__name__)

class TestControllerButtons(JoycontrolPlugin):
    async def push_all_buttons(self):
        button_list = [
            'a', 'b', 'x', 'y',
            'l', 'r', 'zl' ,'zr',
            'l_stick', 'r_stick',
            'minus', 'plus',
            'up', 'down', 'right', 'left', 
            # 'capture', 'home'
        ]

        logger.info(button_list)
        for button in button_list:
            await self.button_push(button)
            await self.wait(0.3)

    async def pushing_button_simultaneous(self):
        logger.info('Push A and B buttons')
        await self.button_push('a', 'b')
        await self.wait(0.3)

        logger.info('Pressing A, B, X, Y buttons')
        await self.button_press('a', 'b', 'x', 'y')
        await self.wait(0.1)

        logger.info('Release only A button')
        await self.button_release('a')
        await self.wait(0.1)

        logger.info('Release B, X, Y buttons')
        await self.button_release('b', 'x', 'y')
        await self.wait(0.1)
    
    async def long_press_button(self):
        logger.info('Press A button for 3.0 seconds')
        await self.button_push('a', press_time_sec=3.0)
        await self.wait(0.3)

    async def run(self):
        logger.info('TEST Controller Buttons Plugin')
        await self.push_all_buttons()
        await self.pushing_button_simultaneous()
        await self.long_press_button()