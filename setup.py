from setuptools import setup

setup(
    name='DolphinUpdater',
    version='1.0.0',
    packages=['dolphin_updater'],
    url='https://github.com/blackmamba97/DolphinUpdater',
    license='MIT',
    author='Max Röhrl',
    author_email='max.roehrl11@gmail.com',
    description='Update the Dolphin emulator',
    requires=['colorama', 'bs4'],
    entry_points={
        'console_scripts': ['dolphin-updater = dolphin_updater.__main__:main']
    }
)
