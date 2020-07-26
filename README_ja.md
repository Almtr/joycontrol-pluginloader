# joycontrol-pluginloader

[English](./README.md) / [日本語](./README_ja.md)

Bluetooth 経由で Nintendo Switch コントローラのエミュレートが行える joycontrol 用のプラグインローダです。  
[GitHub - mart1nro/joycontrol](https://github.com/mart1nro/joycontrol)

## インストール

- joycontrol のインストール  
  詳細: [GitHub - mart1nro/joycontrol - README.md](https://github.com/mart1nro/joycontrol/blob/master/README.md)

    ```sh
    $ sudo apt install python3-dbus libhidapi-hidraw0
    $ git clone https://github.com/mart1nro/joycontrol.git
    $ sudo pip3 install joycontrol/
    ```

- joycontrol-pluginloader のインストール

    ```sh
    $ git clone https://github.com/Almtr/joycontrol-pluginloader
    $ sudo pip3 install joycontrol-pluginloader/
    ```

## joycontrol の Proコントローラをペアリングする

1. Nintendo Switch の「持ちかた/順番を変える」メニューを開く

    HOME > コントローラー > 持ちかた/順番を変える

1. スクリプトを実行する

    ```sh
    $ sudo joycontrol-pluginloader.py plugins/tests/PairingController.py
    ```

    実行結果:  

    ```sh
    $ sudo joycontrol-pluginloader.py plugins/tests/PairingController.py
    [17:03:13] joycontrol.server create_hid_server::58 WARNING - [Errno 98] Address already in use
    [17:03:13] joycontrol.server create_hid_server::60 WARNING - Fallback: Restarting bluetooth due to incompatibilities with the bluez "input" plugin. Disable the plugin to avoid issues. See https://github.com/mart1nro/joycontrol/issues/8.
    [17:03:13] joycontrol.server create_hid_server::65 INFO - Restarting bluetooth service...
    [17:03:14] joycontrol.device set_name::69 INFO - setting device name to Pro Controller...
    [17:03:14] joycontrol.device set_class::61 INFO - setting device class to 0x002508...
    [17:03:14] joycontrol.server create_hid_server::84 INFO - Advertising the Bluetooth SDP record...
    [17:03:14] joycontrol.server create_hid_server::94 INFO - Waiting for Switch to connect... Please open the "Change Grip/Order" menu.
    [17:03:16] joycontrol.server create_hid_server::98 INFO - Accepted connection at psm 17 from ('01:23:45:67:89:AB', 17)
    [17:03:16] joycontrol.server create_hid_server::100 INFO - Accepted connection at psm 19 from ('01:23:45:67:89:AB', 19)
    [17:03:18] root _reply_to_sub_command::295 INFO - received output report - Sub command SubCommand.REQUEST_DEVICE_INFO
    [17:03:18] root _reply_to_sub_command::295 INFO - received output report - Sub command SubCommand.SET_SHIPMENT_STATE
    [17:03:18] root _reply_to_sub_command::295 INFO - received output report - Sub command SubCommand.SPI_FLASH_READ
    [17:03:18] root _reply_to_sub_command::295 INFO - received output report - Sub command SubCommand.SPI_FLASH_READ
    [17:03:18] root _reply_to_sub_command::295 INFO - received output report - Sub command SubCommand.SET_INPUT_REPORT_MODE

    <snip>

    [17:04:04] root _reply_to_sub_command::295 INFO - received output report - Sub command SubCommand.SET_NFC_IR_MCU_CONFIG
    [17:04:04] root _reply_to_sub_command::295 INFO - received output report - Sub command SubCommand.SET_PLAYER_LIGHTS
    [17:04:04] JoycontrolPlugin.loader load_plugin::9 INFO - Loading: plugins/tests/PairingController.py
    [17:04:05] plugins/tests/PairingController.py run::11 INFO - Pairing completed.
    ```

    > 注意:  
    > 「01:23:45:67:89:AB」 は、Nintendo Switch Bluetooth Mac address です。この Mac address は、後で使用します。

## 使い方

- 基本的な使い方

    ```
    $ sudo joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> <Joycontrol Plugin path>
    ```

- オプション

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

## プラグインの作り方

- ファイルを作成する (例: ``SamplePlugin.py``)

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

- ``SamplePlugin.py`` をロードし、実行する 

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

## プラグイン

### TestControllerButotns

コントローラのボタンが正常に動作しているかを確認する。

1. 「ボタンの動作チェック」メニューを開く

    HOME > 設定 > コントローラーとセンサー > 入力デバイスの動作チェック > ボタンの動作チェック

1. joycontrol-pluginloader で TestControllerButtons.py を実行する

    ```
    $ sudo joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> plugins/tests/TestControllerButtons.py 
    ```

### TestControllerSticks

コントローラのスティックが正常に動作しているかを確認する。

1. 「スティックの補正」メニューを開く

    HOME > 設定 > コントローラーとセンサー > スティックの補正

1. joycontrol-pluginloader で TestControllerSticks.py を実行する

    ```
    $ sudo joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> plugins/tests/TestControllerSticks.py 
    ```

### RepeatA

Aボタンを繰り返し押す。

- joycontrol-pluginloader で RepeatA.py を実行する

    ```
    $ sudo joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> plugins/utils/RepeatA.py 
    ```

### SimpleMacro

指定されたボタンを順番に押す。

- joycontrol-pluginloader で SimpleMacro.py を実行する

    ```
    $ sudo joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> plugins/utils/SimpleMacro.py --plugin-options a b x y up down left right
    ```

## 参考

- [GitHub - mart1nro/joycontrol](https://github.com/mart1nro/joycontrol)
- [Discord - Joy-Con Droid](https://discord.com/invite/SQNEx9v)
- [GitHub Gist - colemickens/amiibo-emulation-with-linux-vm.md](https://gist.github.com/colemickens/b08d1a339f4483c6b3c08e739d6cf5d0)