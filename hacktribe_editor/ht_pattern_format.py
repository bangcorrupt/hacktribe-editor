from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging
from construct import Struct, Bytes, Default, Union, Seek

part = Union(
    0,
    'bytes' / Default(Bytes(0x330), bytes(0x330)),
    'struct' / Default(Bytes(0x330), bytes(0x330)),
)

pattern = Union(
    0,
    'bytes' / Default(Bytes(0x4100), bytes(0x4100)),
    'struct' / Struct(
        'header' / Default(Bytes(0x100), bytes(0x100)),
        Seek(0x900),
        'part' / Default(part[16], [None] * 16),
    ),
)

allpat = Union(
    0,
    'bytes' / Default(Bytes(250 * 0x4100), bytes(250 * 0x4100)),
    'struct' / Struct('pattern' / Default(pattern[250], [None] * 250), ),
)
