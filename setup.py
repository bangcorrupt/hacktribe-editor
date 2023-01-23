from setuptools import setup, find_packages

setup(
    name='hacktribe_editor',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'mido',
        'construct @ https://github.com/construct/construct/archive/master.zip',
        'cloup',
        'click-repl',
        'click-spinner',
        'pyfiglet',
        'pyyaml',
        'python-rtmidi',
    ],
    data_files=[('hacktribe_editor/ht_editor_config.yaml',
                 ['hacktribe_editor/ht_editor_config.yaml'])],
    entry_points={
        'console_scripts': [
            'ht-cli = ht_cli.ht_cli:cli',
        ],
    },
)
