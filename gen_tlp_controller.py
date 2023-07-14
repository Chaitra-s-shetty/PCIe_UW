# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import sys
from migen import *
from migen.fhdl import verilog
from litepcie.common import *
from litepcie.core.common import *
from litepcie.tlp.common import *
from litepcie.tlp.controller import LitePCIeTLPController


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        module_name = "tlp_controller_"
        # Module instance ----------------------------------------------------------------
        tlp_controller = LitePCIeTLPController(data_width=64, address_width=32, max_pending_requests=8,
                                               cmp_bufs_buffered=True)
        ios = set()
        ios = set(tlp_controller.master_in.sink.flatten()) |set(tlp_controller.master_out.source.flatten()) | set(tlp_controller.master_out.sink.flatten()) |set(tlp_controller.master_in.source.flatten())
        # ios.add(tlp_controller.tag_queue.source)
        # ios.add(tlp_controller.req_queue.sink)
        # ios.add(tlp_controller.cmp_bufs)
        # ios.add(tlp_controller.cmp_sink)
        # ios.add(tlp_controller.cmp_source)
        verilog.convert(tlp_controller, ios, name=module_name).write(module_name + ".v")
        print("Finished generating", module_name + ".v")


if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

