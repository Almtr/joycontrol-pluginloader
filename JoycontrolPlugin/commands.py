import math
import asyncio
import logging

from joycontrol.controller_state import button_push, button_press, button_release
from joycontrol.command_line_interface import ControllerCLI

logger = logging.getLogger(__name__)

MAX_STICK_POWER = 0xFFF/2

class JoycontrolCommands:
    def __init__(self, controller_state):
        self.cli = ControllerCLI(controller_state)
        self.controller_state = controller_state
        self.__max_stick_power = MAX_STICK_POWER
    
    @property
    def max_stick_power(self):
        return self.__max_stick_power

    def __calc_stick_position(self, angle, power):
        angle = (angle + 180) %  360 * -1

        rad = math.radians(angle)
        x = power * math.cos(rad)
        y = power * math.sin(rad)

        # Adjust the position of the circle.
        stick_radius = MAX_STICK_POWER
        h_val = x + stick_radius
        v_val = y + stick_radius
        return int(h_val), int(v_val)

    async def stick(self, stick, direction=None, angle=None, power=MAX_STICK_POWER):
        if direction == 'center':
            angle = 0
            power = 0
        elif direction == 'left':
            angle = 0
        elif direction == 'up':
            angle = 90
        elif direction == 'right':
            angle = 180
        elif direction == 'down':
            angle = 270
        
        if angle is None:
            raise ValueError('Missing angle')

        logger.debug(f'Stick: {stick}, {angle}, {power}')
        h_val, v_val = self.__calc_stick_position(angle, power)
        await self.cli.cmd_stick(stick, 'horizontal', h_val)
        await self.cli.cmd_stick(stick, 'vertical', v_val)

    async def left_stick(self, direction=None, angle=None, power=MAX_STICK_POWER):
        await self.stick('left', direction, angle, power)

    async def right_stick(self, direction=None, angle=None, power=MAX_STICK_POWER):
        await self.stick('right', direction, angle, power)

    async def button_press(self, *buttons):
        logger.debug('Press {}'.format(', '.join(buttons)))
        await button_press(self.controller_state, *buttons)
    
    async def button_release(self, *buttons):
        logger.debug('Release {}'.format(', '.join(buttons)))
        await button_release(self.controller_state, *buttons)

    async def button_push(self, *buttons, press_time_sec=0.1):
        await self.button_press(*buttons)
        await self.wait(press_time_sec)
        await self.button_release(*buttons)

    async def wait(self, sec):
        logger.debug(f'Wait: {sec}')
        await asyncio.sleep(sec)