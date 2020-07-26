# joycontrol-pluginloader

[English](./README.md) / [日本語](./README_ja.md)

This is a plugin loader for joycontrol that can emulate Nintendo Switch controller over Bluetooth.  
[GitHub - mart1nro/joycontrol](https://github.com/mart1nro/joycontrol)

## Installation

- Install joycontrol  
  Details: [GitHub - mart1nro/joycontrol - README.md](https://github.com/mart1nro/joycontrol/blob/master/README.md)

    ```sh
    $ sudo apt install python3-dbus libhidapi-hidraw0
    $ git clone https://github.com/mart1nro/joycontrol.git
    $ sudo pip3 install joycontrol/
    ```

- Install joycontrol-pluginloader

    ```sh
    $ git clone https://github.com/Almtr/joycontrol-pluginloader
    $ sudo pip3 install joycontrol-pluginloader/
    ```

## Pairing the Pro Controller of joycontrol

1. Open the "Change Grip/Order" menu of the Nintendo Switch

    Home > Controllers > Change Grip/Order

1. Run the script

    ```sh
    $ sudo python3 joycontrol/run_controller_cli.py PRO_CONTROLLER
    ```

## Usage

- Basic Usage

    ```
    $ sudo joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> <Joycontrol Plugin path>
    ```

- Options

    ```
    usage: joycontrol-pluginloader.py [-h]
                                      [-p [PLUGIN_OPTIONS [PLUGIN_OPTIONS ...]]]
                                      [-d DEVICE_ID] [-r RECONNECT_BT_ADDR] [-v]
                                      plugin

    positional arguments:
      plugin                joycontrol plugin path

    optional arguments:
      -h, --help            show this help message and exit
      -p [PLUGIN_OPTIONS [PLUGIN_OPTIONS ...]], --plugin-options [PLUGIN_OPTIONS [PLUGIN_OPTIONS ...]]
                            joycontrol plugin options
      -d DEVICE_ID, --device_id DEVICE_ID
      -r RECONNECT_BT_ADDR, --reconnect_bt_addr RECONNECT_BT_ADDR
                            The Switch console Bluetooth address, for reconnecting
                            as an already paired controller
      -v, --verbose
    ```

## How to create a plugin

- Create a file (e.g. ``SamplePlugin.py``)

    ```python
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
    ```

- Load and run ``SamplePlugin.py``

    ```sh
    $ sudo joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> plugins/samples/SamplePlugin.py arg1 arg2

    <snip>

    [13:30:00] JoycontrolPlugin.loader load_plugin::9 INFO - Loading: plugins/samples/SamplePlugin.py
    [13:30:00] plugins/samples/SamplePlugin.py run::8 INFO - This is sample joycontrol plugin!
    [13:30:00] plugins/samples/SamplePlugin.py run::10 INFO - Plugin Options: ['arg1', 'arg2']
    [13:30:00] plugins/samples/SamplePlugin.py run::12 INFO - Push the A Button
    [13:30:01] plugins/samples/SamplePlugin.py run::16 INFO - Tilt the left stick down
    [13:30:01] __main__ _main::45 INFO - Stopping communication...
    ```

## Sample Plugins

### TestControllerButtons

Check if the controller buttons are working properly.

1. Open the "Test Controller Buttons" menu

    Home > System Settings > Controllers and Sensors > Test Input Devices > Test Controller Buttons

1. Run TestControllerButtons.py with joycontrol-pluginloader

    ```
    $ sudo joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> plugins/samples/TestControllerButtons.py 
    ```

### TestControllerSticks

Check if the controller sticks are working properly.

1. Open the "Calibrate Control Sticks" menu

    Home > System Settings > Controllers and Sensors > Calibrate Control Sticks

1. Run TestControllerSticks.py with joycontrol-pluginloader

    ```
    $ sudo joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> plugins/samples/TestControllerSticks.py 
    ```

### RepeatA

Pushing the "A Button" repeatedly.

- Run RepeatA.py with joycontrol-pluginloader

    ```
    $ sudo joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> plugins/samples/RepeatA.py 
    ```

### SimpleMacro

Press the specified buttons in sequence.

- Run SimpleMacro.py with joycontrol-pluginloader

    ```
    $ sudo joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> plugins/samples/SimpleMacro.py --plugin-options a b x y up down left right
    ```

## References

- [GitHub - mart1nro/joycontrol](https://github.com/mart1nro/joycontrol)
- [Discord - Joy-Con Droid](https://discord.com/invite/SQNEx9v)
- [GitHub Gist - colemickens/amiibo-emulation-with-linux-vm.md](https://gist.github.com/colemickens/b08d1a339f4483c6b3c08e739d6cf5d0)