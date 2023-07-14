import sys
from migen import *
from migen.fhdl import verilog
from litex.soc.interconnect import stream
from litex.soc.interconnect.csr import *
from litepcie.common import *
from litepcie.tlp.common import *
from litepcie.frontend.dma import descriptor_layout, LitePCIeDMAWriter, LitePCIeDMAReader
from litex.soc.interconnect.csr import *
from litepcie.tlp.depacketizer import LitePCIeTLPDepacketizer
from litepcie.tlp.packetizer import LitePCIeTLPPacketizer
from litepcie.core.crossbar import LitePCIeCrossbar
from litepcie.frontend.dma import LitePCIeDMAScatterGather
from litepcie.frontend.dma import LitePCIeDMADescriptorSplitter
from litepcie.frontend.dma import LitePCIeDMAReader
from litepcie.frontend.dma import LitePCIeDMAWriter
from litepcie.frontend.dma import LitePCIeDMALoopback
from litepcie.frontend.dma import LitePCIeDMASynchronizer
from litepcie.frontend.dma import LitePCIeDMABuffering
from litepcie.frontend.dma import LitePCIeDMAStatus
from litepcie.frontend.dma import LitePCIeDMA
from litepcie.core import LitePCIeEndpoint
from litepcie.core.msi import LitePCIeMSI
from test.common import seed_to_data
from test.model.host import *
from test.model.phy import PHY# define main function
def main():
    args = sys.argv[1:]
    if len(args) == 1:
        # rx_tx = int(args[0])
        # PHY -----------------------------------------------------------------------------
        phy = PHY(data_width=128, id=0, bar0_size=1 * MB, debug=False)
        # Endpoint ------------------------------------------------------------------------
        endpoint = LitePCIeEndpoint(phy,
                                    address_width=32,
                                    max_pending_requests=8
                                    )
        # main module instance
        # LitePCIeDMA
        dma_pcie = LitePCIeDMA(phy, endpoint, table_depth = 256, address_width=32, with_writer=True, with_reader=True, with_loopback=False, with_synchronizer=False, with_buffering=False, buffering_depth=256 * 8, writer_buffering_depth=None, reader_buffering_depth=None, with_monitor=False, with_status=False, with_writer_splitter_buffer=True, with_reader_splitter_buffer=True)
        module_name = 'dma_pcie_' 
        ios = set()
        ios = set(dma_pcie.sink.flatten()) | set(dma_pcie.source.flatten())
        print("generate PCIe_DMA_main module=", args[0])
        verilog.convert(dma_pcie, ios, name=module_name).write(module_name + '.v')
        print("Finished generating", module_name, ".v")

if __name__ == "__main__":
    main()
