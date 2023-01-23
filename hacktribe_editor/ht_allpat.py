from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging
from hacktribe_editor.ht_format import HtFormat
from hacktribe_editor.ht_pattern_format import allpat as allpat_fmt
from hacktribe_editor.ht_pattern import HtPattern
from copy import deepcopy


@log_debug
def main():
    allpat = HtAllpat()



class HtAllpat(HtFormat):
    fmt = allpat_fmt

    @log_debug
    def __init__(self, data=None):
        super().__init__(data)

        self.pattern = [HtPattern(p['bytes']) for p in self.struct['pattern']]


if __name__ == "__main__":
    main()
