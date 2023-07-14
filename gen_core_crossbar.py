import sys
from migen import *
from migen.fhdl import verilog

from litepcie.common import *
from litepcie.core.common import *
from litepcie.tlp.controller import LitePCIeTLPController
from litepcie.core.crossbar import LitePCIeCrossbar


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        address_decoder = lambda a:1
        slave_port_num = int(args[0])
        master_port_num = int(args[0])
        module_name = 'crossbar_' + str(master_port_num) + '_' + str(slave_port_num)
        # Module instance ----------------------------------------------------------------
        crossbar = LitePCIeCrossbar(data_width=32, address_width=32, max_pending_requests=8, cmp_bufs_buffered=True)
        ios = set()
        for i in range(master_port_num):
            pcie_master_port = crossbar.get_master_port()
            ios|=(set(pcie_master_port.sink.flatten())) 
        for i in range(slave_port_num):
            pcie_slave_port = crossbar.get_slave_port(address_decoder)
            ios|=(set(pcie_slave_port.source.flatten()))
        crossbar.do_finalize()
        ios|=(set(crossbar.master.source.flatten()))
        ios|=(set(crossbar.slave.sink.flatten()))
        # ios.add(crossbar.user_masters)
        # ios.add(crossbar.user_slaves)
        verilog.convert(crossbar, ios, name=module_name).write(module_name + ".v")
        print("Finished generating", module_name + ".v")


if __name__ == "__main__":
    main()

