import mido
import yaml
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from pathlib import Path

module_path = Path(__file__).parent
config_path = module_path / 'ht_editor_config.yaml'

# config_path = Path('./ht_editor_config.yaml')


def open_config(path=config_path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def write_config(conf, path=config_path):
    with open(path, 'w') as f:
        f.write(yaml.dump(conf, sort_keys=False))


def get_midi_inputs():
    return mido.get_input_names()


if __name__ == '__main__':
    main()
