import logging
from hacktribe_editor.ht_format import HtFormat
from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging


@log_debug
def main():
    part = HtPart()


class HtPart(HtFormat):
    fmt = None  # ht_part_fmt

    @log_debug
    def __init__(self, data=None):
        # super().__init__(data)
        self.index = HtPart.count
        HtPart.count += 1

        # self.patch = [HtPatch() for p in self.patch]
        # self.seq = [HtSequence() for s in self.seq]


if __name__ == "__main__":
    main()
