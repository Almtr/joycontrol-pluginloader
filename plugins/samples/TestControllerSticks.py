import logging
from JoycontrolPlugin import JoycontrolPlugin

logger = logging.getLogger(__name__)

class TestControllerSticks(JoycontrolPlugin):
    async def test_left_stick(self):
        await self.button_push('l_stick')
        await self.wait(1.0)

        logger.info('up, down, left, right')
        for direction in ['up', 'down', 'left', 'right']:
            await self.left_stick(direction)
            await self.wait(1.0)

        logger.info('Rotate')
        for angle in range(360):
            await self.left_stick(angle=angle)
            await self.wait(0.01)

        logger.info('Rotate low power')
        power = self.max_stick_power / 2
        for angle in range(360):
            await self.left_stick(angle=angle, power=power)
            await self.wait(0.01)

        await self.left_stick('center')
        await self.wait(1.0)

        await self.button_push('b')
        await self.wait(1.0)

    async def test_right_stick(self):
        await self.button_push('r_stick')
        await self.wait(1.0)

        logger.info('up, down, left, right')
        for direction in ['up', 'down', 'left', 'right']:
            await self.right_stick(direction)
            await self.wait(1.0)

        logger.info('Rotate')
        for angle in range(360):
            await self.right_stick(angle=angle)
            await self.wait(0.01)

        logger.info('Rotate low power')
        power = self.max_stick_power / 2
        for angle in range(360):
            await self.right_stick(angle=angle, power=power)
            await self.wait(0.01)

        await self.right_stick('center')
        await self.wait(1.0)

        await self.button_push('b')
        await self.wait(1.0)

    async def run(self):
        logger.info('TEST Control Sticks Plugin')
        await self.test_left_stick()
        await self.test_right_stick()