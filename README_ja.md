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

1. Open the "Change Grip/Order" menu of the Nintendo Switch

    Home > Controllers > Change Grip/Order

1. Run the script

    ```sh
    $ sudo python3 joycontrol/run_controller_cli.py PRO_CONTROLLER
    ```

## 使い方

- 基本的な使い方

    ```
    $ sudo python3 joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> <Joycontrol Plugin path>
    ```

- オプション

    ```
    usage: joycontrol-pluginloader.py [-h] [-d DEVICE_ID] [-r RECONNECT_BT_ADDR]
                                      [-v]
                                      plugin [options [options ...]]

    positional arguments:
      plugin                joycontrol plugin path
      options               joycontrol plugin options

    optional arguments:
      -h, --help            show this help message and exit
      -d DEVICE_ID, --device_id DEVICE_ID
      -r RECONNECT_BT_ADDR, --reconnect_bt_addr RECONNECT_BT_ADDR
                            The Switch console Bluetooth address, for reconnecting
                            as an already paired controller
      -v, --verbose
    ```

## プラグインの作り方

- ファイルを作成する (e.g. ``SamplePlugin.py``)

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
    $ sudo python3 joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> plugins/samples/SamplePlugin.py arg1 arg2

    <snip>

    [13:30:00] JoycontrolPlugin.loader load_plugin::9 INFO - Loading: plugins/samples/SamplePlugin.py
    [13:30:00] plugins/samples/SamplePlugin.py run::8 INFO - This is sample joycontrol plugin!
    [13:30:00] plugins/samples/SamplePlugin.py run::10 INFO - Plugin Options: ['arg1', 'arg2']
    [13:30:00] plugins/samples/SamplePlugin.py run::12 INFO - Push the A Button
    [13:30:01] plugins/samples/SamplePlugin.py run::16 INFO - Tilt the left stick down
    [13:30:01] __main__ _main::45 INFO - Stopping communication...
    ```

## サンプルプラグイン

### TestControllerButotns

コントローラのボタンが正常に動作ししているかを確認する。

1. 「ボタンの動作チェック」メニューを開く

    HOME > 設定 > コントローラーとセンサー > 入力デバイスの動作チェック > ボタンの動作チェック

1. joycontrol-pluginloader で TestControllerButtons.py を実行する

    ```
    $ sudo python3 joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> plugins/samples/TestControllerButtons.py 
    ```

### TestControllerSticks

コントローラのスティックが正常に動作ししているかを確認する。

1. 「スティックの補正」メニューを開く

    HOME > 設定 > コントローラーとセンサー > スティックの補正

1. joycontrol-pluginloader で TestControllerSticks.py を実行する

    ```
    $ sudo python3 joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> plugins/samples/TestControllerSticks.py 
    ```

### RepeatA

Aボタンを繰り返し押す。

- joycontrol-pluginloader で RepeatA.py を実行する

    ```
    $ sudo python3 joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> plugins/samples/RepeatA.py 
    ```

### SimpleMacro

指定されたボタンを順番に押す。

- joycontrol-pluginloader で SimpleMacro.py を実行する

    ```
    $ sudo python3 joycontrol-pluginloader.py -r <Switch Bluetooth Mac address> plugins/samples/SimpleMacro.py a b x y up down left right
    ```

## 参考

- [GitHub - mart1nro/joycontrol](https://github.com/mart1nro/joycontrol)
- [Discord - Joy-Con Droid](https://discord.com/invite/SQNEx9v)
- [GitHub Gist - colemickens/amiibo-emulation-with-linux-vm.md](https://gist.github.com/colemickens/b08d1a339f4483c6b3c08e739d6cf5d0)