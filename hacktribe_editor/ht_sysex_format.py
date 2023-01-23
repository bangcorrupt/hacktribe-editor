from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging
from construct import *

msg_id = Default(
    Enum(
        Int8ul,
        current_pattern_request=0x10,
        pattern_request=0x1c,
        global_request=0x0e,
        pattern_write=0x11,
        current_pattern_dump=0x40,
        pattern_dump=0x4c,
        global_dump=0x51,
        read_cpu_ram=0x52,
        set_write_address=0x53,
        write_cpu_ram=0x54,
        read_flash=0x55,
        write_flash=0x56,
        data_format_error=0x26,
        data_load_complete=0x23,
        data_load_error=0x24,
        write_complete=0x21,
        write_error=0x22,
    ), 0x10)

none = Struct(Default(Bytes(0), bytes(0)))

pattern_index = Struct('index' / Default(Int16ul, 0x00), )

address = Struct('address' / Hex(Default(Int32ul, 0xffffffff)), )

mem_addr_len = Struct('addr_len' / Default(Bytes(10), bytes(10)))

data = Struct('data' / OffsettedEnd(-1, Default(GreedyBytes, bytes(0))))

pat_index_data = Struct(
    'index' / Default(Int16ul, 0x00),
    'data' / OffsettedEnd(-1, Default(GreedyBytes, bytes(0))),
)

sysex_body = Switch(this.msg_id, {
    'current_pattern_request': none,
    'pattern_request': pattern_index,
    'global_request': none,
    'pattern_write': pattern_index,
    'current_pattern_dump': data,
    'pattern_dump': pat_index_data,
    'global_dump': data,
    'read_cpu_ram': mem_addr_len,
    'set_write_address': mem_addr_len,
    'write_cpu_ram': data,
    'read_flash': mem_addr_len,
    'write_flash': data,
    'data_format_error': none,
    'data_load_complete': none,
    'data_load_error': none,
    'write_complete': none,
    'write_error': none,
},
                    default=none)

sysex_head = Struct(
    'manu_id' / Default(Int8ul, 0x42),
    'global_channel' / Hex(Default(Int8ul, 0x30)),
    Padding(1),
    'product_id' / Hex(Default(Int16ub, 0x124)),
)

sysex = Struct(
    'status' / Hex(Default(Int8ul, 0xf0)),
    'head' / sysex_head,
    'msg_id' / msg_id,
    'body' / sysex_body,
    'eox' / Hex(Default(Int8ul, 0xf7)),
)
