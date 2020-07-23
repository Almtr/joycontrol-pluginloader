import os
import logging

from importlib.machinery import SourceFileLoader

logger = logging.getLogger(__name__)

def load_plugin(plugin, controller_state, *plugin_options):
    logger.info(f'Loading: {plugin}')
    module = SourceFileLoader(plugin, plugin).load_module()
    plugin_name = os.path.splitext(os.path.basename(plugin))[0]
    joycontrol_plugin = module.__dict__[plugin_name](controller_state, *plugin_options)
    return joycontrol_plugin
