import argparse
import asyncio
import logging
import os

from importlib.machinery import SourceFileLoader

from joycontrol import logging_default as log, utils
from joycontrol.controller import Controller
from joycontrol.memory import FlashMemory
from joycontrol.protocol import controller_protocol_factory
from joycontrol.server import create_hid_server

logger = logging.getLogger(__name__)

class PluginLoader:
    def __init__(self):
        self.transport = None


    def __load_plugin(self, plugin, controller_state, *plugin_options):
        logger.info(f'Loading: {plugin}')
        module = SourceFileLoader(plugin, plugin).load_module()
        plugin_name = os.path.splitext(os.path.basename(plugin))[0]
        joycontrol_plugin = module.__dict__[plugin_name](controller_state, *plugin_options)
        return joycontrol_plugin


    async def start(self, args):
        # Create memory containing default controller stick calibration
        spi_flash = FlashMemory()

        # Get controller name to emulate from arguments
        controller = Controller.from_arg('PRO_CONTROLLER')

        with utils.get_output(path=None, default=None) as capture_file:
            factory = controller_protocol_factory(controller, spi_flash=spi_flash)
            ctl_psm, itr_psm = 17, 19
            transport, protocol = await create_hid_server(factory, reconnect_bt_addr=args.reconnect_bt_addr,
                                                          ctl_psm=ctl_psm,
                                                          itr_psm=itr_psm, capture_file=capture_file,
                                                          device_id=args.device_id)

            controller_state = protocol.get_controller_state()
            self.transport = transport

            try:
                # waits until controller is fully connected
                await controller_state.connect()
                joycontrol_plugin = self.__load_plugin(args.plugin, controller_state, args.plugin_options)
                await joycontrol_plugin.run()
            except Exception as e:
                logger.error(e)
            finally:
                logger.info('Stopping communication...')
                await transport.close()
                self.transport = None
                self.joycontrol_cmd = None


    async def stop(self):
        if self.transport:
            logger.info('Stopping communication...')
            self.transport = None


def main():
    # check if root
    if not os.geteuid() == 0:
        raise PermissionError('Script must be run as root!')

    parser = argparse.ArgumentParser()
    parser.add_argument('plugin', type=str, help='joycontrol plugin path')
    parser.add_argument('-p', '--plugin-options', nargs='*', help='joycontrol plugin options')
    parser.add_argument('-d', '--device_id')
    parser.add_argument('-r', '--reconnect_bt_addr', type=str, default=None,
                        help='The Switch console Bluetooth address, for reconnecting as an already paired controller')
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        log.configure()
    else:
        log.configure(console_level=logging.INFO)
    
    loop = asyncio.get_event_loop()
    loader = PluginLoader()

    try:
        loop.run_until_complete(loader.start(args))
    except KeyboardInterrupt:
        loop.run_until_complete(loader.stop())