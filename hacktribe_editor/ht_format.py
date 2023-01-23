from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging
from pathlib import Path
from copy import deepcopy
import json
import yaml
import logging
from construct import Hex, HexDump, GreedyBytes
from hacktribe_editor import ht_fmt_utils as fmt_utils
from hacktribe_editor.ht_fmt_utils import dict_to_container, container_to_dict, remove_hidden_keys, filter_dict
from hacktribe_editor.ht_fmt_utils import open_bin, yaml_to_bin, json_to_bin, refresh_struct
from hacktribe_editor import ht_fx_preset_format as fxp_fmt
from hacktribe_editor import ht_fx_ram_format as fxr_fmt
from hacktribe_editor import ht_fx_edit_utils as fxed_utils
from hacktribe_editor import ht_logging


@log_debug
def main():
    fxeb = HtIFXEditBuffer()


# FIX - remove union and make struct top level. Build bytes fresh from dict when required
class HtFormat:

    fmt = None
    write_fext = '.bin'
    count = 0
    read_ftypes = {
        'bin': open_bin,
        'ifx': open_bin,
        'mfx': open_bin,
        'yml': yaml_to_bin,
        'yaml': yaml_to_bin,
        'json': json_to_bin,
    }

    @log_debug
    def __init__(self, data=None):
        '''Default initialises from bytes'''
        self.log = logging.getLogger(__name__)
        self.log.info("Initialise %s", self.__class__.__name__)

        self.index = self.__class__.count
        self.__class__.count += 1

        if data is None:
            data = self.fmt.build({})

        container = self.fmt.parse(data)
        dic = container_to_dict(container)
        self.__dict__.update(dic)

    @classmethod
    @log_debug
    def from_bytes(cls, data):
        return cls(data)

    @classmethod
    @log_debug
    def from_container(cls, container):
        data = cls.fmt.build(container)
        return cls(data)

    @classmethod
    @log_debug
    def from_dict(cls, dic):
        data = cls.fmt.build(dic)
        return cls(data)

    @classmethod
    @log_debug
    def from_json(cls, jsn):
        dic = json.load(jsn)
        data = cls.fmt.build(dic)
        return cls(data)

    @classmethod
    @log_debug
    def from_yaml(cls, yml):
        dic = yaml.safe_load(yml)
        data = cls.fmt.build(dic)
        return cls(data)

    @classmethod
    @log_debug
    def from_file(cls, path, ftype=None):
        path = Path(path)
        ftype = path.suffix[1:].lower()
        if ftype in cls.read_ftypes.keys():
            data = cls.read_ftypes[ftype](path)
        return cls(data)

    @property
    @log_debug
    def dict(self):
        return filter_dict(self.fmt, self.__dict__)

    @property
    @log_debug
    def bytes(self):
        return self.fmt.build(self.dict)

    @property
    @log_debug
    def container(self):
        return dict_to_container(self.fmt, self.dict)

    @property
    @log_debug
    def json(self, indent=False):
        if indent:
            return json.dumps(self.format_dict, indent=indent)
        return json.dumps(self.dict)

    @property
    @log_debug
    def yaml(self):
        return yaml.dump(self.dict, sort_keys=False)

    @property
    @log_debug
    def hex(self):
        return HexDump(GreedyBytes).parse(self.bytes)


class HtFXPreset(HtFormat):
    fmt = fxp_fmt.preset.struct

    @property
    @log_debug
    def dict(self):
        dic = filter_dict(self.fmt, self.__dict__)
        dic = {k: v for k, v in dic.items() if not k[:4] in ('unk_', 'slot')}

        # Move control map to last position
        dic['control_map'] = dic.pop('control_map')

        return dic


class HtFXEditBuffer(HtFormat):
    fmt = fxr_fmt.ifx_buffer.struct


class HtMFXEditBuffer(HtFXEditBuffer):
    fmt = fxr_fmt.mfx_buffer.struct


class HtIFXEditBuffer(HtFXEditBuffer):
    fmt = fxr_fmt.ifx_buffer.struct


if __name__ == '__main__':
    main()
