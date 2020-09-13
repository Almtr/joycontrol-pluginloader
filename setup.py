
from setuptools import setup, find_packages

README = open('README.md', 'r').read()

setup(
    name='joycontrol-pluginloader',
    version='0.4',
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/almtr/joycontrol-pluginloader',
    author='almtr',
    description='PluginLoader for mart1nro/joycontrol',
    packages=find_packages(),
    install_requires=[
        'hid', 'aioconsole', 'dbus-python', 'crc8'
    ],
    entry_points={
        'console_scripts': [
            'joycontrol-pluginloader=JoycontrolPlugin.loader:main',
        ],
    },
)
