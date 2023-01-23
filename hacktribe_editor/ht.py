import logging

from hacktribe_editor.ht_format import HtIFXEditBuffer
from hacktribe_editor.ht_format import HtMFXEditBuffer
from hacktribe_editor.ht_allpat import HtAllpat
from hacktribe_editor.ht_logging import log_debug
from hacktribe_editor import ht_logging


@log_debug
def main():
    ht = Ht()



class Ht:

    @log_debug
    def __init__(
        self,
        allpat=None,
        ifxp=None,
        mfxp=None,
        ifxe=None,
        mfxe=None,
        allsamp=None,
    ):
        self.log = logging.getLogger(__name__)
        self.log.info("Initialise Ht")

        ifxe = [None] * 0x20 if ifxe is None else ifxe
        self.ifxe = [
            HtIFXEditBuffer(ifx) if ifx is not None else HtIFXEditBuffer()
            for ifx in ifxe
        ]

        self.mfxe = HtMFXEditBuffer(
            mfxe) if mfxe is not None else HtMFXEditBuffer()

        allsamp = [] if allsamp is None else allsamp
        self.sample = [HtSample(samp) for samp in allsamp]

        self.allpat = HtAllpat(allpat)


if __name__ == "__main__":
    main()
