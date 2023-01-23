import logging
from hacktribe_editor.ht_part import HtPart
from hacktribe_editor.ht_format import HtFormat
from hacktribe_editor.ht_pattern_format import pattern as pat_fmt
from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging


@log_debug
def main():
    pattern = HtPattern()



class HtPattern(HtFormat):
    fmt = pat_fmt

    @log_debug
    def __init__(self, data=None):
        super().__init__(data)

        self.part = [HtPart(p['bytes']) for p in self.struct['part']]


if __name__ == "__main__":
    main()
